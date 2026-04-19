from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import time
from datetime import datetime
from collections import deque
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Log ve Sayaçlar ─────────────────────────
request_log = deque(maxlen=100)
total_requests = 0
total_threats = 0

# ── Model ───────────────────────────────────
MODEL_PATH = "api_threat_model.joblib"
model = None

# Tehdit kararı için eşik
THRESHOLD = 0.88

# Eğitimde kullandığın feature sırası
FEATURE_COLS = [
    "http_status",
    "response_time_ms",
    "http_method_enc",
    "status_class",
    "hour_of_day",
    "payload_length",
    "is_bot_agent",
    "has_payload",
    "payload_threat_score",
    "endpoint_sensitivity",
    "is_night_time",
    "is_error",
    "slow_request",
    "night_high_method",
    "bot_sensitive_ep",
    "error_with_payload",
    "threat_signal_sum",
    "composite_risk",
]


def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Model yüklendi")
    else:
        print("⚠️ Model yok → simülasyon modu aktif")


load_model()


# ── Request Model ───────────────────────────
class APIRequest(BaseModel):
    ip_address: str
    endpoint: str
    http_method: str
    status_code: int
    user_agent: str
    response_time_ms: float
    payload: Optional[str] = None


# ── Feature Engineering ─────────────────────
def extract_features(req: APIRequest) -> dict:
    payload = req.payload or ""
    payload_lower = payload.lower()
    endpoint_lower = req.endpoint.lower().strip()
    ua_lower = req.user_agent.lower().strip()
    current_hour = datetime.now().hour

    # HTTP Method encoding
    method_risk = {"GET": 1, "POST": 2, "PUT": 3, "PATCH": 4, "DELETE": 5}
    http_method_enc = method_risk.get(req.http_method.upper(), 1)

    # Bot agent tespiti
    bot_agents = [
        "sqlmap",
        "loic",
        "python-requests",
        "python-urllib",
        "go-http-client",
        "nikto",
        "nmap",
        "curl",
        "wget",
        "bot",
    ]
    is_bot_agent = int(any(b in ua_lower for b in bot_agents))

    # Payload özellikleri
    has_payload = int(len(payload) > 0)
    payload_length = len(payload)

    threat_keywords = [
        "or 1=1",
        "drop table",
        "alert(",
        "onerror=",
        "union select",
        "/etc/passwd",
        "rm -rf",
        "<script>",
    ]
    payload_threat_score = sum(1 for kw in threat_keywords if kw in payload_lower)

    # Endpoint hassasiyeti
    sensitive_endpoints = {
        "/api/admin": 5,
        "/api/payment": 4,
        "/api/token": 4,
        "/api/users": 3,
        "/api/login": 2,     # önce çok yüksekti, düşürdük
        "/api/orders": 2,
        "/api/profile": 2,
        "/api/cart": 1,
        "/api/search": 1,
        "/api/products": 1,
    }
    endpoint_sensitivity = sensitive_endpoints.get(endpoint_lower, 1)

    # HTTP durum bilgisi
    http_status = int(req.status_code)
    status_class = http_status // 100
    is_error = int(http_status >= 400)

    # Saat bilgisi
    hour_of_day = current_hour
    is_night_time = int(current_hour >= 22 or current_hour < 6)

    # Yavaş istek
    slow_request = int(float(req.response_time_ms) > 800)

    # Kombinasyon özellikleri
    night_high_method = int(is_night_time == 1 and http_method_enc >= 4)
    bot_sensitive_ep = int(is_bot_agent == 1 and endpoint_sensitivity >= 4)
    error_with_payload = int(is_error == 1 and has_payload == 1)

    # Özet sinyal
    threat_signal_sum = (
        is_bot_agent
        + payload_threat_score
        + night_high_method
        + bot_sensitive_ep
        + error_with_payload
        + int(endpoint_sensitivity >= 4)
        + slow_request
        + is_error
    )

    # Composite risk
    composite_risk = (
        payload_threat_score * 4
        + is_bot_agent * 3
        + bot_sensitive_ep * 3
        + endpoint_sensitivity * 2
        + night_high_method * 2
        + error_with_payload * 2
        + is_error * 1
        + slow_request * 1
    )

    return {
        "http_status": http_status,
        "response_time_ms": float(req.response_time_ms),
        "http_method_enc": http_method_enc,
        "status_class": status_class,
        "hour_of_day": hour_of_day,
        "payload_length": payload_length,
        "is_bot_agent": is_bot_agent,
        "has_payload": has_payload,
        "payload_threat_score": payload_threat_score,
        "endpoint_sensitivity": endpoint_sensitivity,
        "is_night_time": is_night_time,
        "is_error": is_error,
        "slow_request": slow_request,
        "night_high_method": night_high_method,
        "bot_sensitive_ep": bot_sensitive_ep,
        "error_with_payload": error_with_payload,
        "threat_signal_sum": threat_signal_sum,
        "composite_risk": composite_risk,
    }


# ── Fallback Model ──────────────────────────
def simulate_prediction(features: dict):
    score = 0.0

    score += min(features["payload_threat_score"], 1) * 0.40
    score += features["is_bot_agent"] * 0.25
    score += features["bot_sensitive_ep"] * 0.10
    score += features["error_with_payload"] * 0.10
    score += features["slow_request"] * 0.05
    score += features["is_error"] * 0.05
    score += (1 if features["endpoint_sensitivity"] >= 4 else 0) * 0.05

    score = min(1.0, score)
    label = int(score >= THRESHOLD)
    return label, float(score)


# ── Attack Type ─────────────────────────────
def detect_attack_type(features: dict, label: int) -> str:
    if label == 0:
        return "Normal"

    if features["payload_threat_score"] >= 1:
        return "Payload Attack"
    if features["is_bot_agent"] == 1 and features["bot_sensitive_ep"] == 1:
        return "Bot Attack"
    if features["is_bot_agent"] == 1:
        return "Bot Activity"
    if features["night_high_method"] == 1:
        return "Suspicious Night Request"
    if features["slow_request"] == 1 and features["is_error"] == 1:
        return "Suspicious Slow Request"
    if features["is_error"] == 1 and features["has_payload"] == 1:
        return "Error With Payload"
    return "Threat Detected"


# ── ANALYZE ENDPOINT ────────────────────────
@app.post("/analyze")
def analyze(req: APIRequest):
    global total_requests, total_threats

    t0 = time.perf_counter()
    features = extract_features(req)

    if model is not None:
        try:
            X = pd.DataFrame([features])

            # Eğitim feature sırası ile birebir eşleştir
            X = X.reindex(columns=FEATURE_COLS, fill_value=0)

            # Modelde feature_names_in_ varsa yine onunla güvenceye al
            if hasattr(model, "feature_names_in_"):
                X = X.reindex(columns=model.feature_names_in_, fill_value=0)

            if hasattr(model, "predict_proba"):
                threat_probability = float(model.predict_proba(X)[0][1])
                label = int(threat_probability >= THRESHOLD)
            else:
                # predict_proba yoksa fallback
                label = int(model.predict(X)[0])
                threat_probability = 1.0 if label == 1 else 0.0

        except Exception as e:
            print("❌ Model error:", e)
            label, threat_probability = simulate_prediction(features)
    else:
        label, threat_probability = simulate_prediction(features)

    attack_type = detect_attack_type(features, label)

    # Kullanıcıya gösterilecek güven:
    # tehditse threat prob, normalse normal prob
    display_confidence = threat_probability if label == 1 else (1.0 - threat_probability)

    elapsed = round((time.perf_counter() - t0) * 1000, 2)

    result = {
        "timestamp": datetime.now().isoformat(),
        "ip": req.ip_address,
        "endpoint": req.endpoint,
        "method": req.http_method,
        "status": req.status_code,
        "label": "Tehdit" if label == 1 else "Normal",
        "label_binary": label,
        "confidence": round(display_confidence, 4),
        "threat_probability": round(threat_probability, 4),
        "threshold": THRESHOLD,
        "attack_type": attack_type,
        "latency_ms": elapsed,
    }

    request_log.append(result)

    total_requests += 1
    if label == 1:
        total_threats += 1

    print("YENI ISTEK GELDI:", result)
    print("FEATURES:", features)
    print("TOPLAM ISTEK:", total_requests, "TOPLAM TEHDIT:", total_threats, "LOG UZUNLUGU:", len(request_log))

    return result


# ── LOG ─────────────────────────────────────
@app.get("/log")
def get_log():
    return list(request_log)


# ── STATS ───────────────────────────────────
@app.get("/stats")
def stats():
    normal_count = total_requests - total_threats
    return {
        "total": total_requests,
        "threats": total_threats,
        "normal": normal_count,
        "threat_rate": (total_threats / total_requests * 100) if total_requests else 0,
        "threshold": THRESHOLD,
    }


# ── RESET ───────────────────────────────────
@app.post("/reset")
def reset_data():
    global total_requests, total_threats

    request_log.clear()
    total_requests = 0
    total_threats = 0

    print("🧹 Sistem sıfırlandı")

    return {
        "success": True,
        "message": "Loglar ve sayaçlar sıfırlandı."
    }


# ── HEALTH ──────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}
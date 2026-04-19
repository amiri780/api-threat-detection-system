# 🛡️ API Threat Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/XGBoost-Enabled-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LightGBM-Enabled-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/CatBoost-Enabled-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" />
</p>

> ML-based binary classifier that detects API threats (SQLi, DDoS, XSS, Brute Force) from request logs — Stacking Ensemble with XGBoost, LightGBM, CatBoost & SHAP explainability.

---

## 📌 İçindekiler

- [Özellikler](#-özellikler)
- [Mimari](#-mimari)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [API Referansı](#-api-referansı)
- [Dashboard](#-dashboard)
- [Model Performansı](#-model-performansı)
- [Veri Seti](#-veri-seti)
- [SHAP Explainability](#-shap-explainability)
- [Katkıda Bulunma](#-katkıda-bulunma)

---

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🔍 **Çoklu Tehdit Tespiti** | SQLi, DDoS, XSS ve Brute Force saldırılarını tanır |
| 🤖 **Stacking Ensemble** | XGBoost + LightGBM + CatBoost meta-modeli |
| 📊 **SHAP Explainability** | Her tahmin için açıklanabilir AI çıktısı |
| ⚡ **Real-Time Dashboard** | Canlı tehdit izleme arayüzü |
| 🌐 **REST API** | FastAPI tabanlı hızlı ve ölçeklenebilir backend |
| 📁 **CSV Log Desteği** | `api_threat.csv` formatında log analizi |

---

## 🏗️ Mimari

```
api-threat-detection-system/
│
├── main.py              # FastAPI backend & model inference
├── dashboard.py         # Real-time monitoring dashboard
├── api_threat.csv       # Eğitim & test veri seti
├── requirements.txt     # Proje bağımlılıkları
└── README.md
```

### Model Pipeline

```
API Request Logs
      │
      ▼
Feature Engineering
      │
      ▼
┌─────────────────────────────┐
│     Stacking Ensemble       │
│  ┌─────────┐ ┌──────────┐  │
│  │ XGBoost │ │ LightGBM │  │
│  └────┬────┘ └────┬─────┘  │
│       │           │         │
│  ┌────┴───────────┴──┐      │
│  │     CatBoost      │      │
│  │   (Meta-Model)    │      │
│  └───────────────────┘      │
└─────────────────────────────┘
      │
      ▼
 SHAP Explanation
      │
      ▼
 Threat / Safe
```

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.9+
- pip

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/amiri780/api-threat-detection-system.git
cd api-threat-detection-system

# 2. Sanal ortam oluştur (önerilir)
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# 3. Bağımlılıkları yükle
pip install -r requirements.txt
```

---

## 🖥️ Kullanım

### API Sunucusunu Başlatmak

```bash
python main.py
```

Sunucu varsayılan olarak `http://localhost:8000` adresinde çalışır.

### Dashboard'u Başlatmak

```bash
python dashboard.py
```

---

## 📡 API Referansı

### `POST /predict`

Tek bir API isteğini analiz ederek tehdit olup olmadığını döndürür.

**Request Body:**

```json
{
  "ip": "192.168.1.1",
  "method": "POST",
  "endpoint": "/login",
  "payload": "admin' OR '1'='1",
  "request_rate": 120,
  "user_agent": "Mozilla/5.0"
}
```

**Response:**

```json
{
  "threat_detected": true,
  "threat_type": "SQLi",
  "confidence": 0.97,
  "shap_explanation": {
    "payload": 0.61,
    "request_rate": 0.22,
    "endpoint": 0.14
  }
}
```

### `GET /health`

Servisin ayakta olup olmadığını kontrol eder.

```json
{ "status": "ok" }
```

### `GET /stats`

Toplam analiz edilen istek sayısı ve tespit istatistiklerini döndürür.

---

## 📊 Dashboard

Real-time tehdit izleme paneli aşağıdaki bilgileri gösterir:

- 📈 Canlı istek trafiği grafiği
- 🚨 Tehdit türü dağılımı (SQLi / DDoS / XSS / Brute Force)
- 🌍 IP bazlı tehdit haritası
- 🔔 Anlık alarm bildirimleri

---

## 🎯 Model Performansı

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| XGBoost | 0.96 | 0.95 | 0.96 | 0.955 |
| LightGBM | 0.97 | 0.96 | 0.97 | 0.965 |
| CatBoost | 0.96 | 0.95 | 0.96 | 0.955 |
| **Stacking Ensemble** | **0.98** | **0.98** | **0.97** | **0.975** |

> ℹ️ Metrikler `api_threat.csv` üzerinde 5-fold cross-validation ile hesaplanmıştır.

---

## 📁 Veri Seti

`api_threat.csv` dosyası aşağıdaki sütunları içermektedir:

| Sütun | Açıklama |
|---|---|
| `ip` | İstemci IP adresi |
| `method` | HTTP metodu (GET, POST, vb.) |
| `endpoint` | Hedef API endpoint |
| `payload` | İstek gövdesi / parametreler |
| `request_rate` | Dakikadaki istek sayısı |
| `user_agent` | Tarayıcı/istemci bilgisi |
| `label` | 0 = Güvenli, 1 = Tehdit |
| `threat_type` | SQLi / DDoS / XSS / BruteForce / None |

---

## 🔬 SHAP Explainability

Her model tahmini için SHAP (SHapley Additive exPlanations) değerleri hesaplanarak hangi özelliğin tehdit kararını ne kadar etkilediği görselleştirilir.

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)
```

---

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun: `git checkout -b feature/yeni-ozellik`
3. Değişikliklerinizi commit edin: `git commit -m 'feat: yeni özellik eklendi'`
4. Branch'i push edin: `git push origin feature/yeni-ozellik`
5. Pull Request açın

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/amiri780">amiri780</a>
</p>

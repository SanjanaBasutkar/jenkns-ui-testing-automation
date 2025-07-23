
# Jenkins UI Automation using Selenium and Pytest

  

This project enables **automated UI verification of Jenkins controllers** and critical job functionalities across multiple environments (such as `sandbox`, `dev2`, `tstdev2`, `prod`). Powered by **Selenium WebDriver** and **Pytest**, it provides end-to-end tests for Jenkins UIs, job execution flows, plugin health, and operational error detection, supporting detailed HTML reporting and seamless CI/CD integration.

  

---

  

## 📌 Objectives

  

-  **Validate** Jenkins controller UI components and core features automatically.

-  **Trigger and verify** key Jenkins jobs (Node Java Version, Plugin Test, Artifact Promotion, etc.).

-  **Detect misconfigurations** and plugin errors, especially on the "Manage Jenkins" page.

-  **Integrate** as a CI/CD Jenkins pipeline (runs daily, Dockerized execution).

-  **Generate** human-readable HTML and (optionally) Allure test reports.

  

---

  

## ⚙️ Tech Stack

  

| Tool / Technology | Purpose |

|-------------------------------|----------------------------------|

| **Python 3.x** | Base scripting language |

| **Selenium WebDriver** | Web automation engine |

| **Pytest** | Testing framework |

| **pytest-html** | Generates HTML test reports |

| **Jenkins** | CI/CD pipeline orchestration |

| **Docker** | Test execution isolation |

| **selenium/standalone-chrome**| Headless Chrome for tests |

  

---

  

## 📁 Folder Structure

  

.

├── pages/

│ ├── NodeJavaVersionJobPage.py # Node version job page

│ ├── PluginTestJobPage.py # Plugin test job page

│ └── PromoteArtifactPage.py # Artifact promotion job page

├── tests/

│ ├── test_00_login.py # Login test

│ ├── test_01_node_java_version.py # Node job test

│ ├── test_02_plugin_test.py # Plugin test job

│ ├── test_03_promote_artifact.py # Artifact promotion

│ ├── test_04_manage_jenkins.py # Manage Jenkins validation

│ └── test_05_plugin_manager_failed_load.py # Plugin load error check

├── conftest.py # Shared fixtures and CLI args

├── requirements.txt # Python dependencies

├── Jenkinsfile # Jenkins pipeline config

└── README.md # Project documentation

  
  

---

  

## 🔧 Setup Instructions

  

### 🐍 Local Setup

  

1.  **Clone the repository**

```

Clone the repo using "git clone http/ssh url"

cd jenkins-ui-testing-automation

```

  

2.  **Create and activate a virtual environment**

```

python3 -m venv venv

source venv/bin/activate # For Windows: venv\Scripts\activate

```

  

3.  **Install dependencies**

```

pip install -r requirements.txt

```

  

---

  

### 🧪 Running Tests Locally

  

To run tests for a specific controller (e.g., dev2):

  

pytest -m "dev2 or all"

--controller dev2

--username your_jenkins_username

--password your_jenkins_password

--html=report.html --self-contained-html

  
  
  

---

  

## 🧪 Test Descriptions

  

| Test Script | Description |

|------------------------------------------|---------------------------------------------|

| `test_00_login.py` | Logs into the Jenkins controller |

| `test_01_node_java_version.py` | Triggers job and checks node Java version |

| `test_02_plugin_test.py` | Triggers plugin test job, inspects output |

| `test_03_promote_artifact.py` | Triggers promotion job, handles errors |

| `test_04_manage_jenkins.py` | Checks /manage page for critical alerts |

| `test_05_plugin_manager_failed_load.py` | Logs plugin manager 'Failed to load' issues |

  

---

  

## 📊 Reports

  

### HTML Report

-  **Automatic**: Generates `report.html` via Pytest and pytest-html

-  **Contains**: Test results summary, (optionally) screenshots, job links, executed controller and user context

  

### Allure Report (Optional)

If Allure is available in CI:

-  **Automatic**: Generates `allure-report` via Pytest and Allure

-  **Contains**: Test results summary, detailed test steps, job links, executed controller and user context

  
  
  

---

  

## 🐳 Jenkins Pipeline Execution

  

- Runs in Docker using `selenium/standalone-chrome` for browser automation

-  **Steps:**

- Sets up Python virtualenv and installs requirements

- Runs all tests via required CLI arguments

- Archives `report.html` and `allure-results` (if generated) as build artifacts

  

**Jenkins Pipeline Parameters:**

  

| Parameter | Description |

|-------------|-------------------------------------|

| CONTROLLER | Controller name (e.g., dev2, prod) |

| USERNAME | Jenkins username for login |

| PASSWORD | Jenkins password or API token |

  

---

  

## 🧠 Pytest CLI Custom Arguments

  

Registered in `conftest.py`:

  

-  `--controller` : Controller short name

-  `--username` : Jenkins username

-  `--password` : Jenkins password or API token

  

All fixtures read from these values for WebDriver/session setup.

  

---

  

## 🔍 Example Job Output

  

-  **Node Java Version**: Expects `Finished: SUCCESS` in console output

-  **Promote Artifact**: Accepts known errors like `No such artifact`

-  **Plugin Manager**: Reports any plugin with “Failed to load”

-  **Manage Jenkins**: Only alerts with `id="redirect-error"` are ignored

  

---



## 📝 Notes

  

- All code and tests are in Python 3.x.

- Designed for multi-environment Jenkins controllers.

- Suitable for both local dev and Jenkins Pipeline (CI/CD) execution.

- See [Jenkins documentation](https://www.jenkins.io) for further configuration and troubleshooting advice[8].

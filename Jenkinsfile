pipeline {
    agent any

    environment {
        SECRET_KEY     = 'django-jenkins-dummy-key-not-for-production'
        DB_NAME        = 'incident_db'
        DB_USER        = 'postgres'
        DB_PASSWORD    = 'ci_password_123'
        DB_HOST        = 'localhost'
        DB_PORT        = '5432'
        ALLOWED_HOSTS  = 'localhost,127.0.0.1'
    }

    stages {

        // ── 1. Clonar el repositori ───────────────────────────────────────────
        stage('📥 Checkout') {
            steps {
                checkout scm
            }
        }

        // ── 2. Instal·lar eines del sistema ───────────────────────────────────
        stage('🔧 Instal·lar dependències del sistema') {
            steps {
                sh '''
                    apt-get update -y
                    # Python & pip
                    apt-get install -y python3 python3-pip python3-venv

                    # PostgreSQL client (per si cal psycopg2)
                    apt-get install -y libpq-dev gcc

                    # Firefox (sense snap) + geckodriver
                    apt-get install -y wget curl gnupg2 ca-certificates
                    install -d -m 0755 /etc/apt/keyrings
                    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg \
                        -O /etc/apt/keyrings/packages.mozilla.org.asc 2>/dev/null || true
                    # Fallback: PPA de Mozilla
                    apt-get install -y software-properties-common
                    add-apt-repository ppa:mozillateam/ppa -y 2>/dev/null || true
                    printf 'Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001\n' \
                        > /etc/apt/preferences.d/mozilla-firefox
                    apt-get update -y
                    apt-get install -y firefox-esr || apt-get install -y firefox

                    # Geckodriver des de GitHub Releases
                    GD_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest \
                        | grep '"tag_name"' | sed 's/.*"v\\([^"]*\\)".*/\\1/')
                    wget -q "https://github.com/mozilla/geckodriver/releases/download/v${GD_VERSION}/geckodriver-v${GD_VERSION}-linux64.tar.gz" \
                        -O /tmp/geckodriver.tar.gz
                    tar -xzf /tmp/geckodriver.tar.gz -C /tmp
                    mv /tmp/geckodriver /usr/local/bin/geckodriver
                    chmod +x /usr/local/bin/geckodriver

                    echo "✅ Firefox: $(firefox --version 2>/dev/null || firefox-esr --version)"
                    echo "✅ Geckodriver: $(geckodriver --version | head -1)"
                '''
            }
        }

        // ── 3. Entorn virtual Python + dependències ───────────────────────────
        stage('📦 Instal·lar dependències Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        // ── 4. Migracions ─────────────────────────────────────────────────────
        stage('🗃️ Migracions Django') {
            steps {
                sh '.venv/bin/python manage.py migrate'
            }
        }

        // ── 5. Tests unitaris ─────────────────────────────────────────────────
        stage('🧪 Tests Unitaris') {
            steps {
                sh '.venv/bin/python manage.py test core.tests --verbosity=2'
            }
        }

        // ── 6. Tests Selenium – Auditoria de Seguretat ────────────────────────
        stage('🛡️ Tests Selenium – Auditoria') {
            steps {
                sh '.venv/bin/python manage.py test core.tests_selenium --verbosity=2'
            }
        }
    }

    // ── Post-accions ──────────────────────────────────────────────────────────
    post {
        success {
            echo '✅ Tots els tests han passat. El sistema és segur.'
        }
        failure {
            echo '❌ Hi ha tests fallits. Revisa els logs per identificar la vulnerabilitat.'
        }
        always {
            echo '📋 Pipeline finalitzat.'
        }
    }
}

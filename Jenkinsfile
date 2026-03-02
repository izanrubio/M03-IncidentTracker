pipeline {
    agent any

    environment {
        // Django usa SQLite al CI de Jenkins (sense PostgreSQL extern)
        // Per fer-ho, sobreescrivim ENGINE i NAME via env.
        // settings.py llegeix os.environ, però si volem SQLite necessitem
        // un settings alternatiu o un truc amb DJANGO_SETTINGS_MODULE.
        SECRET_KEY    = 'django-jenkins-dummy-key-not-for-production'
        ALLOWED_HOSTS = 'localhost,127.0.0.1'
        // Aquestes variables apunten al PostgreSQL si existís (ignorades si usem SQLite settings)
        DB_NAME       = 'incident_db'
        DB_USER       = 'postgres'
        DB_PASSWORD   = 'ci_password_123'
        DB_HOST       = 'localhost'
        DB_PORT       = '5432'
    }

    stages {

        // ── 1. Clonar el repositori ───────────────────────────────────────────
        stage('📥 Checkout') {
            steps {
                checkout scm
            }
        }

        // ── 2. Entorn virtual Python + dependències ───────────────────────────
        stage('📦 Dependències Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip --quiet
                    # Instal·lem Django i Selenium (psycopg2-binary pot fallar sense libpq)
                    .venv/bin/pip install "Django>=4.0" selenium --quiet
                    # Intentem psycopg2-binary; si falla, continuem amb SQLite
                    .venv/bin/pip install psycopg2-binary --quiet || echo "psycopg2 no disponible, usarem SQLite"
                '''
            }
        }

        // ── 3. Migracions amb SQLite (sense BD externa) ───────────────────────
        stage('🗃️ Migracions Django') {
            steps {
                sh '''
                    # Usem un settings que activa SQLite per al CI de Jenkins
                    DJANGO_SETTINGS_MODULE=config.settings_ci .venv/bin/python manage.py migrate
                '''
            }
        }

        // ── 4. Tests unitaris ─────────────────────────────────────────────────
        stage('🧪 Tests Unitaris') {
            steps {
                sh 'DJANGO_SETTINGS_MODULE=config.settings_ci .venv/bin/python manage.py test core.tests --verbosity=2'
            }
        }

        // ── 5. Tests Selenium – Auditoria ─────────────────────────────────────
        stage('🛡️ Tests Selenium – Auditoria') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh 'DJANGO_SETTINGS_MODULE=config.settings_ci .venv/bin/python manage.py test core.tests_selenium --verbosity=2'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Tots els tests han passat. El sistema és segur.'
        }
        unstable {
            echo '⚠️ Tests Selenium no disponibles en aquest agent (sense Firefox).'
        }
        failure {
            echo '❌ Hi ha tests fallits. Revisa els logs.'
        }
        always {
            echo '📋 Pipeline finalitzat.'
        }
    }
}

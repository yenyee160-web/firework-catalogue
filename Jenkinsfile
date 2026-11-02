pipeline {
  agent any
  environment {
    TEST_ENV = 'ci'
    BASE_URL = 'http://127.0.0.1:8000'
    WHATSAPP_NUMBER = '60123456789'
    DJANGO_DEBUG = '1'
  }
  stages {
    stage('Install') {
      steps {
        sh 'python3 -m pip install --user "poetry>=2,<3"'
        sh 'poetry install --no-interaction'
        sh 'cd frontend && npm ci && npm run build'
        sh 'poetry run playwright install --with-deps chromium'
      }
    }
    stage('Test') {
      steps {
        sh '''mkdir -p artifacts
          poetry run python backend/manage.py runserver 127.0.0.1:8000 --noreload > artifacts/server.log 2>&1 &
          echo $! > artifacts/server.pid
          sleep 4
          poetry run pytest tests/api tests/unit tests/e2e --browser chromium --tracing on --video on --screenshot only-on-failure --output artifacts/playwright --junitxml=artifacts/junit.xml --html=artifacts/report.html --self-contained-html
        '''
      }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'artifacts/*.xml'
      archiveArtifacts allowEmptyArchive: true, artifacts: 'artifacts/**'
    }
  }
}

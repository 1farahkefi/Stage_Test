pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask_app_test'
        CONTAINER_NAME = 'flask_test_container'
        DATABASE_URL = 'postgresql+psycopg2://postgres.ckbimfasdfzgiduhonty:SagemCom01%@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Run Flask Container') {
            steps {
                sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                sh "sleep 5"
            }
        }

        stage('Tester si Flask répond') {
            steps {
                sh '''
                    success=0
                    for i in {1..10}; do
                        status=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000)
                        if [ "$status" -eq 200 ]; then
                            success=1
                            break
                        fi
                        sleep 1
                    done
                    if [ "$success" -ne 1 ]; then
                        echo "Flask ne répond pas"
                        exit 1
                    fi
                '''
            }
        }

        stage('Lancer tests Behave Ederson') {
            steps {
                sh "docker exec ${CONTAINER_NAME} python -m behave tests/Ederson/features"
            }
        }

        stage('Lancer tests Behave Livebox7') {
            steps {
                sh "docker exec ${CONTAINER_NAME} python -m behave tests/Livebox7/features"
            }
        }

        stage('Arrêter et Supprimer le conteneur') {
            steps {
                sh "docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}"
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
    }
}

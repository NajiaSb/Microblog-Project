pipeline {
    agent any
     environment {
       CONTAINER_NAME = "microblog"
       IMAGE_NAME = "microblogapp"
       JOB_NAME = "Microblog App"
       BUILD_URL = "http://54.173.6.81:5000/"
    }

    stages {
        stage('Checkout') {
           steps {
               checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url:'git@github.com:NajiaSb/Microblog-Project.git']]])
           }
       }
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'sudo docker build --tag $IMAGE_NAME .'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh 'sudo docker stop $CONTAINER_NAME || true'
                sh 'sudo docker rm $CONTAINER_NAME || true'
                sh 'sudo docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME'
            }
        }
    }
    post {
        failure {
            mail to: "ikram2121ali@gmail.com", subject: "Failed Deployment", body: "${env.BUILD_URL}"
        }
    }
}

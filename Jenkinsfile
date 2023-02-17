pipeline {
   agent any

   environment {
       CONTAINER_NAME = "myapp1"
       IMAGE_NAME = "flaskappv2"
       JOB_NAME = "MicroBlog-App"
       BUILD_URL = "http://3.14.82.212:5001/"

   }

   stages {
       stage('Checkout') {
           steps {
               checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ebinsaad/Flask-Docker-App.git']]])
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
               sh 'sudo docker run -d -p 5001:5000 --name $CONTAINER_NAME flaskappv2'
           }
       }
   }

    post {
        failure {
            mail to: "ikram2121ali@gmail.com, groupmember1@example.com, groupmember2@example.com", 
                 subject: "Failed Deployment", 
                 body: "${env.BUILD_URL}"
        }
    }
}

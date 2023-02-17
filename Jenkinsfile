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
                 sh 'sudo docker run -d -p 5001:5000 --name $CONTAINER_NAME $IMAGE_NAME'
                 sh 'sudo docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME'
             }
         }
     

     
  post {
    failure {
        emailext body: "Deployment of ${env.JOB_NAME} failed. Build URL: ${env.BUILD_URL}", 
                 subject: "Failed Deployment: ${env.JOB_NAME}", 
                 to: "ikram2121ali@gmail.com"
    }
 }
 }

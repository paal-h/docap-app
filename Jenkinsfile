pipeline {

    agent none
    //check every minute for changes
    triggers {
        pollSCM('*/1 * * * *')
    }

    stages {
    //Build goes here
        stage('Build') {
            agent {
                kubernetes {
                    label 'jenkinsrun'
                    defaultContainer 'builder'
                    yaml """
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: builder
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: kaniko-docker-config
        mountPath: /kaniko/.docker
  volumes:
      - name: kaniko-docker-config
      projected:
        sources:
        - secret:
        name: harbor-docap-key
          items:
            - key: .dockerconfigjson
              path: config.json
"""
                }
            }

            steps {
                script {
                    sh """/kaniko/executor -f `pwd`/Dockerfile \
                       -c `pwd` \
                       --insecure \
                       --skip-tls-verify \
                       --cache=true \
                       --destination=harbor.docap.io/docap/app:${env.BUILD_ID}
                       """
                }
            } //steps

        } //stage(build)
        //Test goes here

        //SonarQube goes here

        //Documentation generation goes here

        //Deploy goes here
        
        //Performance testing goes here
        } //stages
} //pipeline
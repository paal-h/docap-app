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
                    sh 'echo $BUILD_ID > VERSION.txt'
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
        stage('Deploy') {
            input {
                message "Should we deploy?"
                ok "Yes, please, that'd be really good"
            }
            agent {
                kubernetes {
                    label 'jenkins-deploy'
                    defaultContainer 'kubectl'
                    containerTemplate(name: 'kubectl', image: "lachlanevenson/k8s-kubectl:v1.13.0", ttyEnabled: true, command: 'cat')
                }
            }
            //replace __version__ with the build number and then apply to our cluster
            steps {
                sh "sh -c \"sed s/__VERSION__/${env.BUILD_ID}/g app-deploy.yml | kubectl apply -f -\""
            }
        }
        //Performance testing goes here
        } //stages
} //pipeline

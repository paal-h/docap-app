def build_tag = "${BUILD_ID}"
def branch_label = "${BRANCH_NAME}"

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
                    if(env.BRANCH_NAME == "master") {
                    //write the version number to a file which gets copied into the container
                        sh 'echo $BUILD_ID > VERSION.txt'
                        sh """/kaniko/executor -f `pwd`/Dockerfile \
                           -c `pwd` \
                           --insecure \
                           --skip-tls-verify \
                           --single-snapshot --destination=harbor.docap.io/docap/app:${build_tag}
                           """
                    } else {
                        //write the branch name and version number to a file which gets copied into the container
                        sh 'echo $BRANCH_NAME.$BUILD_ID > VERSION.txt'
                        sh 'echo $BRANCH_NAME > BRANCH.txt'
                        // remove the feature/ if this is part of branch name, using + as sed separator
                        sh "sed -i s+feature/++g VERSION.txt"
                        sh "sed -i s+feature/++g BRANCH.txt"
                        // replace all / with _ in branch name, using + as sed separator
                        sh "sed -i s+/+_+g VERSION.txt"
                        sh "sed -i s+/+_+g BRANCH.txt"
                        build_tag = readFile('VERSION.txt').trim()
                        branch_label = readFile('BRANCH.txt').trim()
                        sh """/kaniko/executor -f `pwd`/Dockerfile \
                           -c `pwd` \
                           --insecure \
                           --skip-tls-verify \
                           --single-snapshot \
                           --destination=harbor.docap.io/docap/app:${build_tag}
                           """
                    }
                }
            } //steps
        } //stage(build)
        //Test goes here
        stage('Test') {
            parallel {
                stage('Static Analysis') {
                //Run this code within our container for this build
                    agent {
                        kubernetes {
                            label 'jenkins-analysis'
                            defaultContainer 'appy'
                            yaml """
apiVersion: v1
kind: Pod
metadata:
  name: appy
spec:
  containers:
  - name: appy
    image: harbor.docap.io/docap/app:${build_tag}
    tty: true
    imagePullPolicy: Always
  imagePullSecrets:
  - name: harbor-docap-key
"""
                        }
                    }

                    //Run pylint on app.py
                    steps {
                        // first install development tools dependencies
                        sh 'pip install -r requirements-dev.txt'
                        sh 'pylint app.py'
                    }
                } //stage(static analysis)
        //SonarQube goes here
            }
        }
        //Documentation generation goes here
        stage('Documentation') {
            agent {
                kubernetes {
                    label 'jenkins-appy'
                    defaultContainer 'appy'
yaml """
apiVersion: v1
kind: Pod
metadata:
  name: appy
spec:
  containers:
  - name: appy
    image: harbor.docap.io/docap/app:${build_tag}
    tty: true
    command: ["cat"]
    imagePullPolicy: Always
  imagePullSecrets:
  - name: harbor-docap-key
"""
                    }
                }
            steps {
                //generate documentation in html format and put in a directory called output
                // only install dev requirements in temporary container
                sh 'pip install -r requirements-dev.txt'
                sh 'sphinx-build -b html . output'
                //tell jenkins we made an HTML report and to publish it
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'output',
                    reportFiles: 'index.html',
                    reportName: 'Sphinx'
                ]
            }
        }
        //Deploy goes here
        stage('Deploy') {
            agent {
                kubernetes {
                    label 'jenkins-deploy'
                    defaultContainer 'kubectl'
                    yaml """
apiVersion: v1
kind: Pod
metadata:
  name: kubectl
spec:
  containers:
  - name: kubectl
    image: lachlanevenson/k8s-kubectl:v1.13.0
    tty: true
    command: ["cat"]
"""
                }
            }
            //replace __version__ with the build number and then apply to our cluster
            steps {
                script{
                    if(env.BRANCH_NAME == "master") {
                       echo "Deploying master"
                        //replace __version__ with the build number and then apply to our cluster
                        sh "sed s/__VERSION__/${build_tag}/g app-deploy.yml | kubectl apply -f -"
                    } else {
                        echo "Deploying branch - ${BRANCH_NAME}"
                        //replace __BRANCH__and __VERSION__ with the build_tag and build_label and then apply to our cluster
                        sh "sed -i s/__BRANCH__/${branch_label}/g app-deploy-branch.yml"
                        sh "sh -c \"sed s/__VERSION__/${build_tag}/g app-deploy-branch.yml | kubectl apply -f -\""
                    }
                }
            }
        }
        //Performance testing goes here
    } //stages
} //pipeline



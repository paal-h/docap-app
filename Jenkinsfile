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
                    containerTemplate(name: 'builder', image: "python:3.8-slim-buster", ttyEnabled: true, command: 'cat')
                }
            }

            steps {
                script {
                    sh "echo dont build, just run"
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
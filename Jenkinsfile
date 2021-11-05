#Jenkinsfile example
pipeline {
    agent any

    environment {
        # Set up environment variables here
    }

    parameters {
         string(name: 'APP_ENV_NAME', defaultValue: 'local' , description: 'Optional parameter to change app environment.', trim: true)
         string(name: 'TESTS_MARKER', defaultValue: 'regression' , description: 'Optional parameter to run tests for different test markers.', trim: true)
         string(name: 'APPLICATION_BRANCH', defaultValue: 'main' , description: 'Optional parameter to change app Branch', trim: true)
         string(name: 'QA_BRANCH', defaultValue: 'main' , description: 'Optional parameter to change test Branch', trim: true)
    }

    stages {
        stage('Checkout qa project repo') {
            steps {
                dir('qa_project_name'){
                    cleanWs()
                    git branch: """${params.QA_BRANCH}""",
                    credentialsId: 'your_credentials_id',
                    url: 'git@github.com:<project_url>'
                }
            }
        }

        stage('Checkout application repo') {
            steps {
                dir('application name'){
                    cleanWs()
                    git branch: """${params.APPLICATION_BRANCH}""",
                    credentialsId: 'orfium-org-ssh',
                    url: 'git@github.com:application_url'
                }
            }
        }

        stage('Build application') {
            steps {
               dir('application_project'){
                script {
                    if (params.APP_ENV_NAME == 'local') {
                        sh """
                        docker-compose -f local.yml -f ../qa_project_name/application-network.yml up --build -d
                        """
                    } else {
                        sh 'exit 0'
                    }
                }
             }
           }
        }

        stage ('Run tavern api tests') {
            steps {
                dir ('qa_project_name'){
                script {
                        sh """
                        APP_ENV_NAME=${params.APP_ENV_NAME} TAG=${params.TESTS_MARKER} HOST=django:8000 docker-compose -f docker-compose.yml -f qa-network.yml up --build --exit-code-from container_name
                        """
                	}
                }
            }
        }
    }
    post {
      always {
        dir('qa_project_name') {
          		sh """
                docker cp allocation-api-tests:/qa-cmo-allocation/api_tests/reports api_tests/reports
                """
           }
        script{
            withCredentials([string(credentialsId: 'GOOGLE_CHAT_KEY_QA_CHANNEL', variable: 			 'GOOGLE_CHAT_KEY_QA_CHANNEL'), string(credentialsId: 'GOOGLE_CHAT_KEY_TEAM_CHANNEL', variable: 'GOOGLE_CHAT_KEY_TEAM_CHANNEL')]) {
              url = """$GOOGLE_CHAT_KEY_QA_CHANNEL,$GOOGLE_CHAT_KEY_TEAM_CHANNEL"""
                }
            }
        dir('application_project'){
                sh """
                docker-compose -f local.yml -f ../qa_project_name/application-network.yml down -v
                """
        }
        dir('qa_project_name') {
           // Copy test reports from container
          		sh """
                docker cp allocation-api-tests:/qa-cmo-allocation/api_tests/reports api_tests/reports
                """
                script {
                        allure([
                                includeProperties: false,
                                jdk: '',
                                properties: [],
                                reportBuildPolicy: 'ALWAYS',
                                report: 'api_tests/reports/allure-report',
                                results: [[path: 'api_tests/reports/allure-api-results']]])
                }
        }
      }
      // Publish test reports to Googlechat
      success {
          googlechatnotification message: "API Tests Jenkins job was *successful*. \\u2705 \nJob name: ${env.JOB_NAME} \n<${env.BUILD_URL}|Build URL> \n<${env.JENKINS_URL}job/Project_Name/job/${env.JOB_BASE_NAME}/${env.BUILD_NUMBER}/allure/|Allure Report> \nTest run on environment: ${params.APP_ENV_NAME}\napplication branch: ${params.APPLICATION_BRANCH_BRANCH}\nqa-branch: ${params.QA_BRANCH}",
          notifySuccess: true,
          url: url
        }
      failure {
          googlechatnotification message: "API Tests Jenkins job *failed*. \\u274c \nJob name: ${env.JOB_NAME} \n<${env.BUILD_URL}|Build URL> \n<${env.JENKINS_URL}job/Project_Name/job/${env.JOB_BASE_NAME}/${env.BUILD_NUMBER}/allure/|Allure Report> \nTest run on environment: ${params.APP_ENV_NAME}\napplication branch: ${params.APPLICATION_BRANCH_BRANCH}\nqa-branch: ${params.QA_BRANCH}",
          notifyFailure: true,
          url: url
      }
      unstable {
          googlechatnotification message: "API Tests Jenkins job was *unstable*. \\u274c \nJob name: ${env.JOB_NAME} \n<${env.BUILD_URL}|Build URL> \n<${env.JENKINS_URL}job/Project_Name/job/${env.JOB_BASE_NAME}/${env.BUILD_NUMBER}/allure/|Allure Report> \nTest run on environment: ${params.APP_ENV_NAME}\napplication branch: ${params.APPLICATION_BRANCH_BRANCH}\nqa-branch: ${params.QA_BRANCH}",
          notifyUnstable: true,
          url: url
    }
  }
}
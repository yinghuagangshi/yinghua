pipeline {
    agent any

    environment {
        REMOTE_SERVER = '47.97.37.145'
        PROJECT_DIR = '/root/yinghua'
        PYTHON_CMD = 'python3.6'
        TEST_FILE = 'test_async.py'  // 明确指定测试文件
    }

    stages {
        stage('Verify Environment') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        echo "=== Python环境验证 ==="
                        ${PYTHON_CMD} --version
                        ${PYTHON_CMD} -m pip list | grep pytest
                        mkdir -p ${PROJECT_DIR}
                    ENDSSH
                    """
                }
            }
        }

        stage('Setup Dependencies') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pip install pytest-asyncio
                        if [ -f requirements.txt ]; then
                            ${PYTHON_CMD} -m pip install -r requirements.txt
                        fi
                    ENDSSH
                    """
                }
            }
        }

        stage('Run Async Tests') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pytest ${TEST_FILE} \
                            --junitxml=test-results.xml \
                            --asyncio-mode=auto \  # 自动处理异步测试
                            -v
                    ENDSSH
                    """
                }
            }
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                }
            }
        }
    }

    post {
        always {
            echo "测试执行完成. 结果: ${currentBuild.currentResult}"
            cleanWs()
        }
        success {
            slackSend color: 'good', message: "SUCCESS: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        failure {
            slackSend color: 'danger', message: "FAILED: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
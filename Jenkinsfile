pipeline {
    agent any

    environment {
        REMOTE_SERVER = '47.97.37.145'
        PROJECT_DIR = '/root/yinghua'
        GIT_REPO = 'https://gitee.com/yinghuagangshi/yinghua.git'
        PYTHON_CMD = '/usr/bin/python3.6'  // 使用绝对路径
        TEST_FILE = 'testcases/unit_tests/test.py'
    }

    stages {
        stage('Clone Code from Gitee') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 拉取代码 ==="
                        mkdir -p ${PROJECT_DIR}
                        cd ${PROJECT_DIR}
                        if [ ! -d .git ]; then
                            git clone ${GIT_REPO} .
                        else
                            git pull
                        fi
                        echo "代码版本: \$(git rev-parse --short HEAD)"
                    '
                    """
                }
            }
        }

        stage('Verify Environment') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 环境验证 ==="
                        export PATH=\$PATH:/root/.local/bin
                        ${PYTHON_CMD} --version
                        ${PYTHON_CMD} -m pip list | grep pytest || echo "pytest未安装"
                    '
                    """
                }
            }
        }

        stage('Setup Dependencies') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 安装依赖 ==="
                        export PATH=\$PATH:/root/.local/bin
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pip install -U pip
                        ${PYTHON_CMD} -m pip install pytest-asyncio
                        if [ -f requirements.txt ]; then
                            ${PYTHON_CMD} -m pip install -r requirements.txt
                        fi
                    '
                    """
                }
            }
        }

        stage('Run Async Tests') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 运行测试 ==="
                        export PATH=\$PATH:/root/.local/bin
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pytest ${TEST_FILE} \
                            --junitxml=test-results.xml \
                            --asyncio-mode=auto \
                            -v
                    '
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
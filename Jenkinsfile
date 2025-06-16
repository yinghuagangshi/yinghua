pipeline {
    agent any

    environment {
        REMOTE_SERVER = '47.97.37.145'          // 远程服务器IP
        PROJECT_DIR = '/root/yinghua'           // 项目部署目录
        GIT_REPO = 'https://gitee.com/yinghuagangshi/yinghua.git'  // Gitee仓库地址
        PYTHON_CMD = '/usr/bin/python3.6'                // Python命令
        TEST_FILE = 'testcases/unit_tests/test.py'             // 测试文件名
    }

    stages {
        // 阶段1：从Gitee拉取代码
        stage('Clone Code from Gitee') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
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
                    ENDSSH
                    """
                }
            }
        }

        // 阶段2：验证环境（Python、依赖等）
        stage('Verify Environment') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        echo "=== 环境验证 ==="
                        ${PYTHON_CMD} --version
                        ${PYTHON_CMD} -m pip list | grep pytest || echo "pytest未安装"
                    ENDSSH
                    """
                }
            }
        }

        // 阶段3：安装依赖
        stage('Setup Dependencies') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        echo "=== 安装依赖 ==="
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pip install -U pip
                        ${PYTHON_CMD} -m pip install pytest-asyncio
                        if [ -f requirements.txt ]; then
                            ${PYTHON_CMD} -m pip install -r requirements.txt
                        fi
                    ENDSSH
                    """
                }
            }
        }

        // 阶段4：运行异步测试
        stage('Run Async Tests') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        echo "=== 运行测试 ==="
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pytest ${TEST_FILE} \
                            --junitxml=test-results.xml \
                            --asyncio-mode=auto \
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

    // 后置处理（通知和清理）
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
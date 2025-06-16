pipeline {
    agent any
    environment {
        // 远程服务器配置
        REMOTE_SERVER = '47.97.37.145'
        PROJECT_DIR = '/root/yinghua'
        GIT_REPO = 'https://gitee.com/yinghuagangshi/yinghua.git'
        PYTHON_CMD = '/usr/bin/python3.6'
        TEST_FILE = 'testcases/unit_tests/test_common.py'

        // 邮件配置
        EMAIL_RECIPIENTS = 'slg112511@163.com'      // 收件人
        EMAIL_REPLY_TO = 'shilingang111@163.com'    // 发件人（回复地址）

        // Allure报告配置
        ALLURE_RESULTS = 'reports/allure-results'
        ALLURE_REPORT = 'reports/allure-report'
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
                            git fetch --all
                            git checkout -B master
                            git reset --hard origin/master
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
                        echo "PATH: \$PATH"
                        which pytest || echo "pytest 未找到"
                        ${PYTHON_CMD} --version
                        ${PYTHON_CMD} -m pip list | grep pytest || echo "pytest未安装"
                        ${PYTHON_CMD} -m pip list | grep allure-pytest || echo "allure-pytest未安装"
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
                        ${PYTHON_CMD} -m pip install pytest pytest-asyncio allure-pytest
                        if [ -f requirements.txt ]; then
                            ${PYTHON_CMD} -m pip install -r requirements.txt
                        fi
                        # 创建报告目录
                        mkdir -p ${PROJECT_DIR}/reports
                        mkdir -p ${PROJECT_DIR}/${ALLURE_RESULTS}
                    '
                    """
                }
            }
        }

        stage('Run Async Tests with Allure') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 运行测试 ==="
                        export PATH=\$PATH:/root/.local/bin
                        cd ${PROJECT_DIR}
                        # 运行测试并生成Allure结果
                        ${PYTHON_CMD} -m pytest ${TEST_FILE} \
                            --junitxml=${PROJECT_DIR}/reports/test-results.xml \
                            --alluredir=${PROJECT_DIR}/${ALLURE_RESULTS} \
                            -v || true
                        echo "测试执行完毕，返回码: \$?"
                    '
                    """
                    // 将测试结果文件从远程服务器复制到本地
                    sh """
                    scp -o StrictHostKeyChecking=no -r root@${REMOTE_SERVER}:${PROJECT_DIR}/${ALLURE_RESULTS} .
                    scp -o StrictHostKeyChecking=no root@${REMOTE_SERVER}:${PROJECT_DIR}/reports/test-results.xml .
                    """
                }
            }
            post {
                always {
                    junit testResults: 'test-results.xml',
                          allowEmptyResults: true,
                          skipPublishingChecks: true,
                          skipMarkingBuildUnstable: true

                    // 生成Allure报告
                    script {
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: "${ALLURE_RESULTS}"]]
                        ])
                    }
                }
            }
        }
    }

    post {
        always {
            // 清理工作空间
            cleanWs()

            // 发送邮件通知
            emailext (
                subject: "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                <h2>${env.JOB_NAME} 构建结果</h2>
                <p><strong>状态:</strong>
                   <span style="color: ${currentBuild.currentResult == 'SUCCESS' ? 'green' : 'red'}">
                   ${currentBuild.currentResult}
                   </span>
                </p>
                <p><strong>构建编号:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>触发原因:</strong> ${currentBuild.getBuildCauses()[0].shortDescription}</p>
                <p><strong>控制台日志:</strong> <a href="${env.BUILD_URL}">点击查看完整日志</a></p>
                <p><strong>Allure报告:</strong> <a href="${env.BUILD_URL}allure">点击查看测试报告</a></p>
                """,
                to: "${env.EMAIL_RECIPIENTS}",
                replyTo: "${env.EMAIL_REPLY_TO}"
            )
        }
    }
}
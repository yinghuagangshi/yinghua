pipeline {
    agent any

    environment {
        REMOTE_SERVER = '47.97.37.145'      // 远程服务器IP
        PROJECT_DIR = '/root/yinghua'       // 项目目录（确保存在）
        PYTHON_CMD = 'python3.6'            // 指定Python版本
        TEST_PATH = 'testcases/unit_tests'  // pytest测试目录
    }

    stages {
        // 阶段1：验证远程环境
        stage('Verify Remote Environment') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex  # 启用详细日志和错误退出
                        echo "=== 环境检查 ==="
                        echo "Python版本: \$(${PYTHON_CMD} --version)"
                        echo "Pytest版本: \$(${PYTHON_CMD} -m pytest --version)"
                        echo "项目目录内容:"
                        ls -la ${PROJECT_DIR} || mkdir -p ${PROJECT_DIR}
                    ENDSSH
                    """
                }
            }
        }

        // 阶段2：同步代码
        stage('Sync Code') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        cd ${PROJECT_DIR}
                        if [ -d .git ]; then
                            git pull origin master
                        else
                            git clone ${env.GIT_URL} .
                        fi
                    ENDSSH
                    """
                }
            }
        }

        // 阶段3：运行pytest测试
        stage('Run pytest') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                        set -ex
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pytest ${TEST_PATH} \
                            --junitxml=test-results.xml \  # 生成JUnit格式报告
                            --maxfail=1 \
                            --disable-warnings \
                            -v           # 显示详细输出
                    ENDSSH
                    """
                }
            }
            post {
                always {
                    // 归档测试报告（可选）
                    junit "${PROJECT_DIR}/test-results.xml"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline执行完成！状态: ${currentBuild.result}"
        }
        success {
            slackSend channel: '#your-channel', message: "✅ 测试通过: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#your-channel', message: "❌ 测试失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
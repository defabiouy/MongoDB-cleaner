def branchName = env.BRANCH_NAME

library identifier: 'shared-pipeline@master', retriever: modernSCM(
        [$class: 'GitSCMSource',
        remote: 'http://<<COMPLETAR>>.git',
        credentialsId: 'COMPLETAR'])

pythonProjectPipeline {
    projectName = "mongodb-cleaner"
    buildImage = "COMPLETAR:1.0"
    projectGroup = "COMPLETAR"
    branch = branchName
}

node('docker-slave') {
checkout scm
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      //git 'https://github.com/sergiobaquero/test1'

   }
   stage('Build') {
      sh 'docker build -t sergiobaquero:trainingmodel .'

   }
   stage('Run') {
    withCredentials([usernamePassword(credentialsId: 'NexusUser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
      echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
      sh '''#!/bin/bash -xe

            git rev-parse HEAD > .commit
            sha=`cat .commit`

            type=${BRANCH_NAME:0:3}

            if [ "$type" == 'PR-' ];
            then
               BRANCH_NAME='PR'
            fi

            docker rm -f entrenamiento || true
            docker run --name entrenamiento  -v "$(pwd)":/code sergiobaquero:trainingmodel
            #curl -v -u $USER:$PASS --upload-file svc.pkl http://172.31.7.247:8081/repository/maven-releases/org/svc/$BUILD_ID/svc-$BUILD_ID.pkl
            curl -v -u $USER:$PASS --upload-file svc.pkl http://172.31.7.247:8081/repository/models/$BRANCH_NAME/$sha/svc.pkl
            docker rm entrenamiento
            rm svc.pkl

            echo "LA BRANCH ES:"
            echo "$BRANCH_NAME"
            echo "JOB"
            echo "$JOB_NAME"
            echo "JOB_BASE_NAME"
            echo "$JOB_BASE_NAME"
            echo "FORK"
            echo "$CHANGE_FORK"
            echo "USER"
            echo "$CHANGE_AUTHOR"




            #curl -v -u $USER:$PASS -X GET http://172.31.7.247:8081/repository/maven-releases/org/svc/$BUILD_ID/svc-$BUILD_ID.pkl --output svc-$BUILD_ID.pkl
            curl -v -u $USER:$PASS -X GET http://172.31.7.247:8081/repository/models/$BRANCH_NAME/$sha/svc.pkl --output svc.pkl

            #mv svc-$BUILD_ID.pkl svc.pkl
            docker rm -f test || true
            docker run --name test  -v "$(pwd)":/code sergiobaquero:trainingmodel python3 ./src/model/test.py
            docker rm test
        '''

    }
   }
   stage('Results') {
        withCredentials([string(credentialsId: 'postgres_insert_user', variable: 'USER')]) {
            sh '''
            precision=`cat .accuracy.txt`
            psql -h 172.31.7.247 -U $USER -d postgres -c """INSERT INTO training VALUES ($BUILD_ID,current_timestamp,'$JOB_NAME',$precision)"""
            '''


        }
   }

}


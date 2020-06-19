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
            start=`date +%s`
            git rev-parse HEAD > .commit
            sha=`cat .commit`

            type=${BRANCH_NAME:0:3}

            if [ "$type" == 'PR-' ];
            then
               BRANCH_NAME='PR'
            fi

            docker rm -f entrenamiento || true
            docker run --name entrenamiento  -v "$(pwd)":/code sergiobaquero:trainingmodel
            model_name=`cat .model_name.txt`

            curl -v -u $USER:$PASS --upload-file $model_name.pkl http://172.31.7.247:8081/repository/models/$model_name/$BRANCH_NAME/$sha/$model_name.pkl
            docker rm entrenamiento
            rm $model_name.pkl

            end=`date +%s`
            traintime=$((end-start))

            echo "$traintime" > .trainduration.txt

      '''
       }
    }
    stage('Test') {
     withCredentials([usernamePassword(credentialsId: 'NexusUser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
      echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
      sh '''#!/bin/bash -xe
            start=`date +%s`


            foo=$(git show -s --pretty=%an)

            echo "EL USUARIO ES:"
            echo "$foo"

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

            sha=`cat .commit`
            model_name=`cat .model_name.txt`
            curl -v -u $USER:$PASS -X GET http://172.31.7.247:8081/repository/models/$model_name/$BRANCH_NAME/$sha/$model_name.pkl --output $model_name.pkl

            docker rm -f test || true
            docker run --name test  -v "$(pwd)":/code sergiobaquero:trainingmodel python3 ./src/model/test.py
            docker rm test

            end=`date +%s`
            testtime=$((end-start))

            echo "$testtime" > .testduration.txt
        '''

    }
   }
   stage('Results') {
        withCredentials([string(credentialsId: 'postgres_insert_user', variable: 'USER')]) {
            sh '''
            precision=`cat .accuracy.txt`
            model_name=`cat .model_name.txt`
            train_duration=`cat .trainduration.txt`
            test_duration=`cat .testduration.txt`
            psql -h 172.31.7.247 -U $USER -d postgres -c """INSERT INTO training VALUES ($BUILD_ID,current_timestamp,'$BRANCH_NAME',$precision,'$model_name',$train_duration,$test_duration,'$CHANGE_AUTHOR')"""
            '''


        }
   }

}


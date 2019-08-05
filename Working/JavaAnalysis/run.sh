mvn package
java -cp target/JavaAnalysis-1.0-SNAPSHOT.jar FunctionExtractor ../test ../temp/test.json
java -cp target/JavaAnalysis-1.0-SNAPSHOT.jar FunctionExtractor ../../../projects/alibaba_fastjson ../temp/comment_code_data/alibaba_fastjson.json

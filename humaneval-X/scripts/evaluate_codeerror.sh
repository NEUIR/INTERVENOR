# This script is for evaluating the functional correctness of the generated codes of HumanEval-X.
# bash scripts/evaluate_humaneval_x.sh <RESULT_FILE> <LANG> <N_WORKERS>
# bash scripts/evaluate_humaneval_x.sh "/data1/wanghanbin/codellama/data/humaneval-X/results/cpp/samples_zeroshot.jsonl" cpp 4
# bash scripts/evaluate_humaneval_x.sh "/data1/wanghanbin/codellama/data/humaneval-X/results/java/samples_zeroshot.jsonl" java 4
# bash scripts/evaluate_humaneval_x.sh "/data1/wanghanbin/codellama/data/humaneval-X/results/js/samples_zeroshot.jsonl" js 4
# bash scripts/evaluate_humaneval_x.sh "/data1/wanghanbin/codellama/data/humaneval-X/results/go/samples_zeroshot.jsonl" go 4
#下面的代码从命令行读取参数，第一个参数是生成的代码的路径，第二个参数是目标语言，第三个参数是并行的进程数，第四个参数是超时时间。
INPUT_FILE=$1  # Path to the .jsonl file that contains the generated codes.
LANGUAGE=$2  # Target programming language, currently support one of ["python", "java", "cpp", "js", "go"]
N_WORKERS=$3  # Number of parallel workers.
TIMEOUT=$4  # Timeout in seconds.

# 这段代码是用来获取当前脚本文件的路径及其所在的目录的路径。
SCRIPT_PATH=$(realpath "$0")  #脚本的绝对路径
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")   #当前脚本所在的目录的路径
MAIN_DIR=$(dirname "$SCRIPT_DIR") #获取脚本所在目录的上一级目录的路径。

echo "$INPUT_FILE"   #打印生成的代码的路径

if [ -z "$N_WORKERS" ]   #判断并行的进程数是否为空，如果为空，则设置为64。 -z 判断字符串是否为空
then
    N_WORKERS=64
fi

if [ -z "$LANGUAGE" ]   #判断目标语言是否为空，如果为空，则设置为python。
then
    LANGUAGE=python
fi

if [ -z "$TIMEOUT" ]    #判断超时时间是否为空，如果为空，则设置为5。
then
    TIMEOUT=5
fi

DATA_DIR=/data1/wanghanbin/codellama/data/codeerror/data/codeerror_python.jsonl

if [ $LANGUAGE = go ]; then     #判断目标语言是否为go，如果是，则设置环境变量。
  export PATH=$PATH:/usr/local/go/bin
fi

if [ $LANGUAGE = cpp ]; then    #判断目标语言是否为cpp，如果是，则设置环境变量。
  export PATH=$PATH:/usr/bin/openssl
fi

CMD="python $MAIN_DIR/humaneval-x/evaluate_humaneval_x.py \
    --input_file "$INPUT_FILE" \
    --n_workers $N_WORKERS \
    --tmp_dir $MAIN_DIR/humaneval-x/ \
    --problem_file $DATA_DIR \
    --timeout $TIMEOUT"

echo "$CMD"
eval "$CMD"
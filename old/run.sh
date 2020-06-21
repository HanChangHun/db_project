# ./run.sh -c 12 -m 24

help() {
    echo "[OPTIONS]          ARG"
    echo "  -c               num_cpu"
    echo "  -m               memory_size"
    echo "  -h               print help"
    exit 0
}

while getopts ":c:m:h" opt; do
    case $opt in
        c) CPU_NUM=$OPTARG;;
        m) MEMORY_SIZE=$OPTARG;;
        h) help;;
    esac
done

MEMORY_SWAP_SIZE=$((MEMORY_SIZE*2))

echo "num_cpu: $CPU_NUM"
echo "momory size: $MEMORY_SIZE"
echo "momory swap size: $MEMORY_SWAP_SIZE"

docker run --name db40 -e POSTGRES_PASSWORD=1234 -dit 40db \
           -m ${MEMORY_SIZE}G \
           --memory-swap ${MEMORY_SWAP_SIZE}G \
           --cpus ${CPU_SHARES}
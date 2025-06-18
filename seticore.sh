mkdir -p seticore_output

for file in et_signals/*.h5; do
    filename=$(basename "$file" .h5)
    seticore "$file" --output "seticore_output/${filename}.dat"
done
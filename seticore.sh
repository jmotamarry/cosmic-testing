mkdir -p seticore_output

for file in /datax/scratch/jaym/synthetic_unresolved_vardrift1_32kHz_snr1_1000.h5; do
    filename=$(basename "$file" .h5)
    seticore "$file" --output "seticore_output/${filename}.dat"
done
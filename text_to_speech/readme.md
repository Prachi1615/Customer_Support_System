# To run the code - run the following command in the terminal
# Update the wake word and file name accordingly

python text_to_speech_script.py --model base --english --energy 300 \
       --pause 0.8 --dynamic_energy --wake_word "sid" \
       --verbose
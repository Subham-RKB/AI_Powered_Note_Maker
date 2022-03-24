from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

def summarize(src_text):
    text = src_text.split(' ')

    model_name = 'google/pegasus-large'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    result = ""
    textSize = len(text)
    cnt = int(textSize / 200)
    for i in range(cnt + 1):
        j = i*100
        cur = ""

        while(j < min((i+1) * 100, textSize)):
            cur += text[j] + ' '
            j += 1

        tokens = tokenizer(cur, truncation=True, padding="longest", return_tensors="pt")
        summary = model.generate(**tokens)
        summarized_text = tokenizer.decode(summary[0])
        result += summarized_text + ' '
        print("hi")

    
    print("Length of text: ",len(text))
    print("Length of summary: ", len(result.split()))
    return result

text = """John McCarthy was born in Boston, Massachusetts, on September 4, 1927, to an Irish immigrant father and a Lithuanian Jewish immigrant mother,[4] John Patrick and Ida (Glatt) McCarthy. The family was obliged to relocate frequently during the Great Depression, until McCarthy's father found work as an organizer for the Amalgamated Clothing Workers in Los Angeles, California. His father came from Cromane, a small fishing village in County Kerry, Ireland.[5] His mother died in 1957.[6]

Both parents were active members of the Communist Party during the 1930s and encouraged learning and critical thinking. Before he attended high school, he got interested in science by reading a translation of a Russian popular science book for children, called 100,000 Whys.[7] John was fluent in the Russian language and made friends with Russian scientists during multiple trips to the Soviet Union but he became disillusioned after making visits to the Soviet Bloc which lead to him becoming a conservative Republican.[8]

McCarthy graduated from Belmont High School two years early.[9] McCarthy was accepted into Caltech in 1944.

McCarthy showed an early aptitude for mathematics; during his teens he taught himself college mathematics by studying the textbooks used at the nearby California Institute of Technology (Caltech). As a result, he was able to skip the first two years of mathematics at Caltech.[10] McCarthy was suspended from Caltech for failure to attend physical education courses.[11] He then served in the US Army and was readmitted, receiving a B.S. in mathematics in 1948.[12]

It was at Caltech that he attended a lecture by John von Neumann that inspired his future endeavors.

McCarthy initially completed graduate studies at Caltech before moving to Princeton University. He received a Ph.D. in mathematics from Princeton in 1951 after completing a doctoral dissertation, titled "Projection operators and partial differential equations", under the supervision of Donald C. Spencer.[13]"""
    
print(summarize(text))
# text to speech
from pyt2s.services import stream_elements


obj = stream_elements.StreamElements()
voices = ['Russell', 'Amy']
data = obj.requestTTS('The poor dog found himself the the house. A boy ran up and saved the dog, giving him many hugs', 'Bianca')

# Good Ones ['Russell', 'Justin', 'Matthew','Salli', 'Zhiyu']


with open('testvoice.mp3', '+wb') as file:
    file.write(data)


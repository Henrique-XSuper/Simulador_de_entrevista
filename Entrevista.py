# Instalar bibliotecas necessárias
!pip install python-docx PyMuPDF ipywidgets

# Imports
import ipywidgets as widgets
from IPython.display import display, clear_output
import fitz  # PyMuPDF
import docx
import io

# Função para extrair texto do currículo
def extract_text_from_file(file):
    name = file['metadata']['name']
    content = file['content']
    if name.endswith('.txt'):
        return content.decode('utf-8', errors='ignore')
    elif name.endswith('.pdf'):
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif name.endswith('.docx'):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "⚠️ Formato de arquivo não suportado."

# Perguntas da entrevista
questions = [
    "Quais são suas principais habilidades técnicas?",
    "Você tem experiência com projetos em equipe?",
    "Como você lida com prazos apertados?",
    "Descreva um desafio profissional que superou.",
    "Você tem experiência com ferramentas de versionamento como Git?"
]

# Interface de upload
resume_upload = widgets.FileUpload(accept='.txt,.pdf,.docx', multiple=False)
start_button = widgets.Button(description="Iniciar Entrevista", button_style='success')

# Campos de resposta
answer_widgets = [widgets.Textarea(placeholder="Digite sua resposta aqui...", layout=widgets.Layout(width='100%')) for _ in questions]
submit_button = widgets.Button(description="Finalizar Entrevista", button_style='primary')

# Função para calcular pontuação
def finalizar_entrevista(b):
    clear_output()
    total_score = 0
    question_count = 0
    print("📋 Resultados da Entrevista:\n")
    for i, answer in enumerate(answer_widgets):
        resposta = answer.value.strip()
        print(f"❓ {questions[i]}")
        if resposta:
            score = min(10, len(resposta) // 10)
            print(f"✅ Resposta: {resposta}")
            print(f"🎯 Pontuação: {score}/10\n")
            total_score += score
            question_count += 1
        else:
            print("⚠️ Resposta vazia. Nenhuma pontuação atribuída.\n")
    if question_count > 0:
        avg_score = round(total_score / question_count, 2)
        print(f"🏁 Entrevista concluída. Pontuação média: {avg_score}/10 em {question_count} perguntas.")
    else:
        print("📭 Nenhuma resposta válida foi pontuada.")

# Função de clique do botão de início
def on_start_clicked(b):
    clear_output()
    if len(resume_upload.value) == 0:
        print("⚠️ Por favor, envie seu currículo primeiro!")
        display(resume_upload, start_button)
        return
    file_data = list(resume_upload.value.values())[0]
    resume_text = extract_text_from_file(file_data)
    print("📄 Currículo processado com sucesso!\n")
    print("🧠 Responda às perguntas abaixo com base no seu currículo:\n")
    for i, q in enumerate(questions):
        display(widgets.HTML(value=f"<b>{q}</b>"))
        display(answer_widgets[i])
    display(submit_button)

# Exibir interface inicial
print("📄 Envie seu currículo (.txt, .pdf, .docx) para iniciar a entrevista:")
display(resume_upload, start_button)
start_button.on_click(on_start_clicked)
submit_button.on_click(finalizar_entrevista)

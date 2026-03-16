from flask import Flask, request, jsonify
from flask_cors import CORS
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/api/planificaciones", methods=["POST"])
def guardar():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "JSON no contiene datos"}), 400

    # Datos generales
    materia = data.get("materia", "").strip()
    curso = data.get("curso", "").strip()
    ciclo = data.get("ciclo", "").strip()
    institucion = data.get("institucion", "").strip()

    docente = data.get("docente", "").strip()
    mail_usuario = data.get("userEmail", "").strip()

    # Seccion 1
    enfoque = data.get("enfoque", "").strip()
    identidad = data.get("identidad", "").strip()
    ejes = data.get("ejes", "").strip()

    # Seccion 2
    profundizacion = data.get("profundizacion", "").strip()
    actividades_inicio = data.get("actividades_inicio", "").strip()

    # Seccion 3
    cuatri1 = data.get("cuatri1", "").strip()
    valoracion1 = data.get("valoracion1", "").strip()
    intensificacion1 = data.get("intensificacion1", "").strip()
    cuatri2 = data.get("cuatri2", "").strip()
    valoracion2 = data.get("valoracion2", "").strip()

    # Seccion 4
    articulacion = data.get("articulacion", "").strip()
    nucleos = data.get("nucleos", "").strip()
    producto = data.get("producto", "").strip()
    keywords = data.get("keywords", "").strip()

    # Seccion 5
    pendientes = data.get("pendientes", "").strip()
    diciembre = data.get("diciembre", "").strip()
    febrero = data.get("febrero", "").strip()

    # Seccion 6
    continuidad = data.get("continuidad", "").strip()
    recursos = data.get("recursos", "").strip()

    # Extras
    attachments = data.get("attachments", [])
    editing_id = data.get("editingId", None)

    if not materia:
        return jsonify({"error": "Falta el campo materia"}), 400

    if not docente:
        return jsonify({"error": "Falta el nombre del docente"}), 400

    # carpeta base
    carpeta_base = "exports"
    os.makedirs(carpeta_base, exist_ok=True)

    # carpeta por docente
    nombre_docente = docente.replace(" ", "_")
    carpeta_docente = os.path.join(carpeta_base, nombre_docente)
    os.makedirs(carpeta_docente, exist_ok=True)

    # nombre archivo pdf
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_pdf = f"{timestamp}_{materia.replace(' ', '_')}.pdf"
    ruta_pdf = os.path.join(carpeta_docente, nombre_pdf)

    # crear pdf
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def titulo(texto):
        pdf.set_font("Arial", "B", 15)
        pdf.cell(0, 10, texto, ln=True)
        pdf.ln(2)

    def subtitulo(texto):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, texto, ln=True)
        pdf.ln(1)

    def campo(label, valor):
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, label, ln=True)

        pdf.set_font("Arial", "", 11)
        texto = valor.strip() if isinstance(valor, str) else str(valor)

        if not texto:
            texto = "-"

        pdf.multi_cell(0, 7, texto)
        pdf.ln(2)

    titulo("Planificación")

    campo("Docente", docente)
    campo("Email", mail_usuario)
    campo("Fecha de generación", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    subtitulo("G. Datos Generales")
    campo("Materia / Espacio Curricular", materia)
    campo("Año / Curso", curso)
    campo("Ciclo Lectivo", ciclo)
    campo("Institución", institucion)

    subtitulo("1. Fundamentación de la Propuesta")
    campo("Enfoque Pedagógico y Capacidades", enfoque)
    campo("Identidad Técnica y Perfil Profesional", identidad)
    campo("Ejes Transversales (ESI, EAI, Saberes Digitales)", ejes)

    subtitulo("2. Período de Inicio (Marzo - Abril)")
    campo("Enfoque de Profundización", profundizacion)
    campo("Actividades de Inicio", actividades_inicio)

    subtitulo("3. Organización por Cuatrimestres")
    campo("Primer Cuatrimestre (Marzo - Julio)", cuatri1)
    campo("Valoración Preliminar - Mayo", valoracion1)
    campo("Intensificación / Profundización - Julio", intensificacion1)
    campo("Segundo Cuatrimestre (Agosto - Diciembre)", cuatri2)
    campo("Valoración Preliminar - Octubre", valoracion2)

    subtitulo("4. Proyectos Interdisciplinarios")
    campo("Articulación de Saberes", articulacion)
    campo("Núcleos Problemáticos", nucleos)
    campo("Producto Final / Impacto", producto)
    campo("Palabras Clave", keywords)

    subtitulo("5. Materias Pendientes e Intensificación")
    campo("Modelos de Organización", pendientes)
    campo("Propuesta Diciembre", diciembre)
    campo("Propuesta Febrero/Marzo", febrero)

    subtitulo("6. Continuidad Pedagógica")
    campo("Planificación Anticipada (mínimo 5 clases)", continuidad)
    campo("Recursos y Materiales", recursos)

    subtitulo("Archivos Adjuntos")
    campo("Cantidad de adjuntos", str(len(attachments)))

    if attachments and isinstance(attachments, list):
        nombres_adjuntos = []
        for archivo in attachments:
            if isinstance(archivo, dict):
                nombre = archivo.get("name", "archivo_sin_nombre")
                nombres_adjuntos.append(f"- {nombre}")
            else:
                nombres_adjuntos.append(f"- {str(archivo)}")

        campo("Detalle de adjuntos", "\n".join(nombres_adjuntos))
    else:
        campo("Detalle de adjuntos", "No se adjuntaron archivos")

    campo("Editing ID", str(editing_id) if editing_id is not None else "-")

    pdf.output(ruta_pdf)

    return jsonify({
        "ok": True,
        "mensaje": "Planificación guardada correctamente",
        "file": ruta_pdf,
        "folder": carpeta_docente,
        "editingId": editing_id
    }), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)

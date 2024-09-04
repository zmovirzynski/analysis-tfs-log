import os
import re

def suggest_fix(error_message):
    if "Invalid argument" in error_message:
        return "Verifique se os parâmetros passados estão corretos e no formato esperado."
    elif "CreatureScript Interface" in error_message:
        return "Verifique os scripts das criaturas e valide se estão de acordo com a documentação."
    elif "Action Interface" in error_message:
        return "Valide as ações e eventos registrados para evitar conflitos ou configurações incorretas."
    elif "OTBM Loader" in error_message:
        return "Verifique a integridade dos arquivos de mapa ou tente carregar um backup."
    elif "attempt to index field" in error_message:
        return "Verifique se a variável referenciada está corretamente inicializada ou se não há valores nulos inesperados."
    elif "stack traceback" in error_message or "Traceback" in error_message:
        return "Rastreie a origem do erro no código e trate exceções de forma adequada."
    else:
        return "Erro desconhecido. Verifique a documentação ou revise o código."

def analyze_logs(log_folder):
    error_pattern = re.compile(r"(ERROR|FATAL|Exception|Traceback|stack traceback)", re.IGNORECASE)
    context_lines = 5
    results = []
    all_errors = []
    
    for root, dirs, files in os.walk(log_folder):
        for file in files:
            if file.endswith(".log"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if error_pattern.search(line):
                            start = max(i - 1, 0)
                            end = min(i + context_lines, len(lines))
                            error_context = lines[start:end]
                            error_message = ''.join(error_context).strip()
                            suggestion = suggest_fix(error_message)
                            results.append((file, error_message, suggestion))
                            all_errors.append(f"Arquivo: {file}\nErro: {error_message}\nSugestão: {suggestion}\n{'-'*50}")
    
    return results, all_errors

def generate_output(log_folder):
    log_analysis_results, all_errors = analyze_logs(log_folder)
    
    output_file = os.path.join(log_folder, "log_error_report.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for error in all_errors:
            f.write(error + "\n")
    
    print(f"Relatório gerado: {output_file}")

log_folder = os.path.dirname(os.path.abspath(__file__))
generate_output(log_folder)

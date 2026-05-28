"""
Módulo de Geração de Relatórios em PDF
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from config.settings import PDF_OUTPUT_DIR


class PDFGenerator:
    """Classe para gerar relatórios em PDF"""
    
    def __init__(self):
        """Inicializa gerador de PDF"""
        self.ensure_output_dir()
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()
    
    def ensure_output_dir(self):
        """Garante que o diretório de saída existe"""
        if not os.path.exists(PDF_OUTPUT_DIR):
            os.makedirs(PDF_OUTPUT_DIR)
    
    def create_custom_styles(self):
        """Cria estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=10,
            spaceBefore=10
        ))
    
    def gerar_relatorio_materiais(self, materiais, movimentacoes):
        """Gera relatório de materiais de informática"""
        filename = f"{PDF_OUTPUT_DIR}relatorio_materiais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
        story = []
        
        # Título
        story.append(Paragraph("Relatório de Materiais de Informática", self.styles['CustomTitle']))
        story.append(Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", self.styles['Normal']))
        story.append(Spacer(1, 0.3*cm))
        
        # Seção de Materiais
        story.append(Paragraph("Materiais Cadastrados", self.styles['CustomHeading']))
        
        # Dados da tabela
        data = [['ID', 'Descrição', 'Categoria', 'Número de Série', 'Quantidade', 'Disponível', 
                 'Valor Unitário', 'Fornecedor', 'Localização']]
        
        for material in materiais:
            data.append([
                str(material.get('id', '')),
                str(material.get('descricao', ''))[:30],
                str(material.get('categoria', '')),
                str(material.get('numero_serie', '')),
                str(material.get('quantidade_total', '0')),
                str(material.get('quantidade_disponivel', '0')),
                f"R$ {material.get('valor_unitario', 0):.2f}",
                str(material.get('fornecedor', ''))[:15],
                str(material.get('localizacao', ''))
            ])
        
        # Criar tabela
        table = Table(data, colWidths=[0.6*cm, 2.5*cm, 1.5*cm, 1.8*cm, 1.2*cm, 1.2*cm, 1.3*cm, 1.5*cm, 1.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*cm))
        
        # Seção de Movimentações
        if movimentacoes:
            story.append(PageBreak())
            story.append(Paragraph("Histórico de Movimentações", self.styles['CustomHeading']))
            
            mov_data = [['ID', 'Material', 'Tipo', 'Quantidade', 'Data', 'Responsável', 'Motivo']]
            
            for mov in movimentacoes[-50:]:  # Ültimas 50 movimentações
                mov_data.append([
                    str(mov.get('id', '')),
                    str(mov.get('descricao', ''))[:20],
                    str(mov.get('tipo_movimentacao', '')),
                    str(mov.get('quantidade', '')),
                    str(mov.get('data_movimentacao', ''))[:10],
                    str(mov.get('responsavel', '')),
                    str(mov.get('motivo', ''))[:15]
                ])
            
            mov_table = Table(mov_data, colWidths=[0.8*cm, 2.5*cm, 1.2*cm, 1.2*cm, 1.5*cm, 1.8*cm, 2*cm])
            mov_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(mov_table)
        
        # Gerar PDF
        doc.build(story)
        return filename
    
    def gerar_relatorio_movimentacao(self, movimentacao):
        """Gera relatório de uma movimentação específica"""
        filename = f"{PDF_OUTPUT_DIR}movimentacao_{movimentacao['id']}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Título
        story.append(Paragraph("Comprovante de Movimentação", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*cm))
        
        # Dados
        info_text = f"""
        <b>ID da Movimentação:</b> {movimentacao.get('id', 'N/A')}<br/>
        <b>Material:</b> {movimentacao.get('descricao', 'N/A')}<br/>
        <b>Tipo:</b> {movimentacao.get('tipo_movimentacao', 'N/A').upper()}<br/>
        <b>Quantidade:</b> {movimentacao.get('quantidade', '0')}<br/>
        <b>Data:</b> {movimentacao.get('data_movimentacao', 'N/A')}<br/>
        <b>Responsável:</b> {movimentacao.get('responsavel', 'N/A')}<br/>
        <b>Motivo:</b> {movimentacao.get('motivo', 'N/A')}<br/>
        <b>Observações:</b> {movimentacao.get('observacoes', 'N/A')}
        """
        
        story.append(Paragraph(info_text, self.styles['Normal']))
        story.append(Spacer(1, 1*cm))
        
        # Assinatura
        story.append(Paragraph("_" * 50, self.styles['Normal']))
        story.append(Paragraph("Assinatura do Responsável", self.styles['Normal']))
        
        doc.build(story)
        return filename


pdf_generator = PDFGenerator()

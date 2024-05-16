from fpdf import FPDF

class PDF(FPDF):
    def draw_dotted_line(self, width=190, gap=1, dot_radius=0.25):
        # Draw a dotted line
        self.set_fill_color(0, 0, 0)  # Set dot color to black
        x_start = self.get_x()
        x_end = x_start + width
        y = self.get_y()
        while x_start < x_end:
            self.ellipse(x_start, y - dot_radius, 2 * dot_radius, 2 * dot_radius, style='F')  # Draw dot
            x_start += gap  # Adjust the gap between dots


    def personal_info(self, name, title, email, phone, linkedin_url):
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, name, 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, title, 0, 1)
        self.cell(0, 10, phone, 0)
        self.cell(-200, 10, email, 0, 0, 'C')
        self.cell(0, 10, linkedin_url, 0, 0, 'R')
        self.ln(10)

    def summary(self, summary):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'SUMMARY', 0, 1)
        self.set_draw_color(0, 0, 0)  
        self.set_line_width(0.5)  
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())  
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, summary)
        self.ln(10)

    def experience(self, experiences):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'EXPERIENCE', 0, 1)
        self.set_line_width(0.5)  
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())  
        self.set_font('Arial', '', 12)
        for index, experience in enumerate(experiences):
            self.cell(0, 10, experience['title'], 0, 1)
            self.cell(0, 10, experience['company'], 0)
            self.cell(0, 10, experience['duration'], 0, 0, 'R')
            self.ln()
            self.multi_cell(0, 10, experience['summary'].replace('•','\u2022'))
            self.ln(5)
            if index != len(experiences) - 1:  # Check if it's not the last iteration
                self.draw_dotted_line()

    def education(self, educations):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'EDUCATION', 0, 1)
        self.set_line_width(0.5)  
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())  
        self.set_font('Arial', '', 12)
        for education in educations:
            self.cell(0, 10, education['course'], 0, 1)
            self.cell(0, 10, education['university'], 0)
            self.cell(0, 10, education['duration'], 0, 0, 'R')
            self.ln()
            self.multi_cell(0, 10, education['summary'].replace('•','\u2022'))
            self.ln(5)

    def skills(self, skills):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'SKILLS', 0, 1)
        self.set_line_width(0.5)  
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())  
        self.set_font('Arial', '', 12)
        self.cell(0, 10, '\t\t\t\t\t'.join(skills), 0, 1)
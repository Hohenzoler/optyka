from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QSyntaxHighlighter, QFont


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkYellow)
        keywordFormat.setFontWeight(QFont.Bold)

        keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
            'class', 'continue', 'del', 'def', 'elif', 'else', 'except', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
            'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 'self'
        ]

        self.highlightingRules = [(QRegularExpression(r'\b' + keyword + r'\b'), keywordFormat) for keyword in keywords]

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegularExpression(r'".*?"'), quotationFormat))
        self.highlightingRules.append((QRegularExpression(r"'.*?'"), quotationFormat))

        functionFormat = QTextCharFormat()
        functionFormat.setForeground(Qt.magenta)
        self.highlightingRules.append((QRegularExpression(r'\b\w+\b(?=\s*\()'), functionFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.gray)
        self.highlightingRules.append((QRegularExpression(r'#.*'), singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.gray)

        self.commentStartExpression = QRegularExpression(r"'''|\"\"\"")
        self.commentEndExpression = QRegularExpression(r"'''|\"\"\"")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = expression.match(text, start + length)

        self.setCurrentBlockState(0)

        if self.previousBlockState() != 1:
            start_comment = self.commentStartExpression.match(text)
            if start_comment.hasMatch():
                self.setCurrentBlockState(1)
                start = start_comment.capturedStart()
                end = start_comment.capturedEnd()
                self.setFormat(start, end - start, self.multiLineCommentFormat)
                start = end
            else:
                start = 0

            while True:
                comment = self.commentEndExpression.match(text, start)
                if not comment.hasMatch():
                    break
                end = comment.capturedStart()
                commentLength = comment.capturedLength()
                self.setFormat(start, end - start + commentLength, self.multiLineCommentFormat)
                start = end + commentLength
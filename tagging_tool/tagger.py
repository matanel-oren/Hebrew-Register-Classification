from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
import sys


INFILE = '../data/chosen/merged_1.txt'
OUTFILE = '../data/tagged/tagged_train_sents.tsv'
TAGGING_INDEX_FILE = 'tagging_index'
sample_num = 1


def end_tagging_session():
	sys.exit()


def on_button_click(label, widget, tag):
	with open(TAGGING_INDEX_FILE, encoding='utf8') as file:
		index = int(file.read()) + 1
	with open(TAGGING_INDEX_FILE, 'w', encoding='utf8') as file:
		file.write(str(index))
	with open(OUTFILE, 'a', encoding='utf8') as file:
		if index != 1:
			file.write('\n')
		file.write(label.text() + '\t' + str(tag))
	with open(INFILE, encoding='utf8') as file:
		sents = file.read().split('\n')
	if len(sents) <= index:
		sys.exit()
	sent = sents[index]
	global sample_num
	sample_num += 1
	widget.setWindowTitle(str(sample_num) + '/100')
	label.setText(sent)

	if sample_num > 100:
		end_tagging_session()


def window():
	app = QApplication([])
	widget = QWidget()

	with open(TAGGING_INDEX_FILE, encoding='utf8') as file:
		index = int(file.read())
	with open(INFILE, encoding='utf8') as file:
		sent = file.read().split('\n')[index]
	label = QLabel(sent)
	label.setWordWrap(True)
	font = QFont()
	font.setBold(False)
	font.setPointSize(17)
	font.setFamily('Ariel')
	label.setFont(font)
	label.setStyleSheet("background-color: white; color: black;")

	low_button = QPushButton('שפה נמוכה - מדוברת, לא תקנית', widget)
	low_button.setFixedHeight(100)
	low_button.setStyleSheet("background-color: red; color: blue;")
	def on_low_button_clicked():
		on_button_click(label, widget, 'casual')
	low_button.clicked.connect(on_low_button_clicked)

	middle_button = QPushButton('שפה תקנית')
	middle_button.setFixedHeight(100)
	middle_button.setStyleSheet("background-color: orange; color: blue;")
	def on_middle_button_clicked():
		on_button_click(label, widget, 'neutral')
	middle_button.clicked.connect(on_middle_button_clicked)

	high_button = QPushButton('שפה גבוהה / מליצית')
	high_button.setFixedHeight(100)
	high_button.setStyleSheet("background-color: green; color: blue;")
	def on_high_button_clicked():
		on_button_click(label, widget, 'formal')
	high_button.clicked.connect(on_high_button_clicked)


	layout = QVBoxLayout()
	layout.addStretch(1)
	layout.addWidget(label, 15)
	layout.addStretch(3)
	layout.addWidget(high_button, 5)
	layout.addStretch(1)
	layout.addWidget(middle_button, 5)
	layout.addStretch(1)
	layout.addWidget(low_button, 5)

	widget.setWindowTitle(str(sample_num) + '/100')
	widget.setGeometry(50, 100, 900, 1000)
	widget.setLayout(layout)
	widget.show()
	app.exec_()


if __name__ == '__main__':
	window()

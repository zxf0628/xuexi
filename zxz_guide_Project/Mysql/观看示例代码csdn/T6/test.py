# import pymysql
#
# db = pymysql.connect(host='localhost',
#                      user='root',
#                      password='Zwq197166',
#                      port=3306,
#                      database='test')
#
#
# cursor = db.cursor()
#
# sql = "select * from sc"
# try:
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     for (sno, cno, grade) in results:
#         print(sno,cno,grade)
# except:
#     print("unable to fetch data")


dic = {'1213':'sadf','121':'sadf'}

for key, value in dic.items():
    print(key,value)

print('1213' in dic)
# s = "insert into my_student(sid,name,sex,address) values({sid},{name},{sex},{address};".format(name='123',sid="213",sex="1235", address= "0998")
# print(s)


# def context_menu_of_events_table(self, pos):
#     """
#             用于在tableWidget中点击右键的触发事件，显示右键菜单
#         :return:
#         """
#     pop_menu = QMenu()
#     add_new_event = pop_menu.addAction('添加新事件')
#     del_selected_event = pop_menu.addAction('删除选中事件')
#
#     action = pop_menu.exec_(self.tag_ui.events_table.mapToGlobal(pos))
#
#     if action == add_new_event:  # 如果选中的是添加新的事件
#         """
#         	如果是添加新行，首先必须先将表格的总行数加1，才能进行后续操作，将表格的行数加1之后，再在新加的行内每一列中添加Item
#
#         """
#
#         cur_total_row = self.tag_ui.events_table.rowCount()
#         cur_row = cur_total_row + 1
#         self.tag_ui.events_table.setRowCount(cur_row)  # 将当前的总行数加1
#
#         self.tag_ui.events_table.setItem(cur_row - 1, 0, QTableWidgetItem("请添加新的事件"))
#         # event_table.setItem(index, 1, QTableWidgetItem(event_node.getAttribute('cause')))
#
#         # 下拉框，默认值为'N'，因为大部分值都为'N'
#         combox_list = ['N', 'Y']
#         combox = QtWidgets.QComboBox()
#         combox.addItems(combox_list)
#         combox.setCurrentIndex(0)
#         # 这个函数可以用来定义所有控件的
#         combox.setStyleSheet('QComboBox{margin:3px;font-family:Times New Roman;font-size:14;border-radius:8px}')
#         self.tag_ui.events_table.setCellWidget(cur_row - 1, 1, combox)
#
#         elif action == del_selected_event:
#         """
#             如果我们选择用.selectedItems()函数来得到当前选中的多行，一定要注意，这个函数返回的是所有选中的item，即返回的item的个数为：选中的行数 * 每一行的item数(我这个代码中有8列，但每行只返回7个item，我也不知道为什么，这一点需要注意一下)。
#              每个item都可以通过.indexFromItem(items).row()得到其所在的行号，再通过.removeRow(row_number)删除对应的行。
#              所以在删除时并不是所有的item都需要用，因为很显然要删除每一行都只需要一个该行的item即可，如果有多个肯定会报错，所以我才做了如下操作，在固定间隔取一个item，保证每一行中都只有一个item保留下来，这样就能保证每个被选中的行都只被删除一次。
#              还有一个需要注意的问题，如果选择多行的话，比如选择的行号为1,2,3,7,9，如果我们从前面开始删除，比如先删除第1行，则剩下的行的行的删除会出现问题，因为第1行删除后，原来的第2行会变成新的第1行，原来的第3行会变成新的第2行，以此类推，这很显然会导致剩余行的删除出现问题。我这里的解决办法是先将要删除的行进行降序排序，从后往前删除则可以保证删除的行不会发生错误。
#
#
#         """
#
#         selected_items = self.main_ui.tuple_events_table.selectedItems()
#         if len(selected_items) == 0:  # 说明没有选中任何行
#             return
#         selected_items = [selected_items[i] for i in range(len(selected_items) - 1, -1, -7)]
#         # 将选定行的行号降序排序，只有从索引大的行开始删除，才不会出现错误
#         for items in selected_items:
#             self.main_ui.tuple_events_table.removeRow(self.main_ui.tuple_events_table.indexFromItem(items).row())
#

from datetime import datetime
from langchain_core.messages import SystemMessage

removing_system_message = SystemMessage(f"""
Sen bir yapay zeka asistanısın ve görevlerin                                       
* Kullanıcı sana silmek istediği bir dosyanın ismini gönderecek
* Bu dosya ismini 'name_of_file_that_will_be_removed' alanına ekle
* Sadece 'name_of_file_that_will_be_removed' alanını doldur ve başka hiçbir şey ekleme.
* Yukarıdaki görevlerin haricinde başka herhangi bir şey yapmamalısın                                                        
                                        """)

def removing_system_message_function():
    return removing_system_message
from es_helpers import delete_meetingpoint_index, delete_wordcloud_index, create_meetingpoint_index, create_wordcloud_index

def run():
    #delete_meetingpoint_index()
    delete_wordcloud_index()
    #create_meetingpoint_index()
    create_wordcloud_index()


run()
import query_detector as qd
import extract_performance_query as epq
import table_classfication as tc
import mail

def main():
    filename = input('Enter filename: ')
    status = qd.detector(filename)
    if status == -1:
        return
    print('Query detection complete')
    epq.performance_query()
    status = tc.generate_result()
    if status == True:
        print('Queries extracted')
        status = mail.send_mail()
        if status:
            print('Mail Sent')
        else:
            print('Mail Not Sent')

if __name__ == '__main__':
    main()
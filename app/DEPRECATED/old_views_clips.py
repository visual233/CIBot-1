
@csrf_exempt
def q(request):
    if request.method == 'POST':
        data = json_load(request.body)
        if data is None:
            return response_write(die(400))

        uid = data.get('uid')
        question = data.get('question')
        if question is None or uid is None:
            return response_write(die(403))
        logger.info('Get [%s]: %s' % (uid, question))

        # AI-Dispatch
        ans = qa_snake(question)
        q = {
            'uid' : uid,
            'keywords' : ans['kw'],
            'question' : question,
        }
        similar_qid=Question.find_alike(q)
        if similar_qid:
            #find the ans to this qid
            #then return it!
            # or maybe save the qid in the value qid
            #the return qid is not the similar qid!!
            ans = Answer.qid_get_ans_con(similar_qid)
            data = {
                'answer' : ans,
                'qid' : similar_qid,
                # so what is qid now??
            }
            return response_write(data)
        else:
            # CI-Dispatch
            qid = update_questionlist(q).qid
            a = {
                'uid': 'QaBot',
                'qid': qid,
                'answer': ans['ans']
            }
            update_answerlist(a)

        ans = Answer.objects.filter(question = qid)
        if ans.exists():
            for final_ans in ans:
                if final_ans:
                    if final_ans.content:
                        data = {
                            'answer': ans[0].content,
                            'qid': qid,
                        }
                        return response_write(data)
        data = {
                #what's this??
            'helpers': ['@dsfsd6s46SDVD', '@DVS68d4DVSvsDVSv4654v6s8'],
            'qid': qid,
        }
        return response_write(data)
    else:
        return response_write(die(405))


@csrf_exempt
def a(request):
    print("in a")
    if request.method == 'POST':
        print("in a")
        data = json_load(request.body)
        if not data:
            return response_write(die(400))

        uid = data.get('uid') or -1
        qid = data.get('qid') or ''
        answer = data.get('answer') or ''
        print('Get <%s>-[%d]: %s' % (uid, qid, answer))

        if not Question.objects.filter(qid = qid).exists():
            return response_write({'info':'The Question you post is not exist!'})

        a = {
            'uid' : uid,
            'qid' : qid,
            'answer' : answer
        }

        update_answerlist(a)

        return response_write(die(200))
    else:
        return response_write(die(405))

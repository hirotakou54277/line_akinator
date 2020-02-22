from tanakinator import line, handler, db
from tanakinator.models import UserStatus, Question, Progress, Answer
from tanakinator.akinator import GameState, get_game_status

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction
)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    user_id = event.source.user_id
    reply_content = []

    user_status = db.session.query(UserStatus).filter_by(user_id=user_id).first()
    if not user_status:
        user_status = UserStatus()
        user_status.user_id = user_id
        user_status.status = 'pending'
        db.session.add(user_status)
        db.session.commit()
    status = GameState(user_status.status)

    if status == GameState.PENDING:
        if message == "はじめる":
            question = Question.query.all()[0]
            if not user_status.progress:
                user_status.progress = Progress()
            user_status.progress.latest_question = question
            user_status.status = GameState.ASKING.value
            db.session.add(user_status)
            db.session.commit()
            items = [
                QuickReplyButton(action=MessageAction(label="はい", text="はい")),
                QuickReplyButton(action=MessageAction(label="いいえ", text="いいえ")),
            ]
            reply_content.append(TextSendMessage(text=question.message, quick_reply=QuickReply(items=items)))

        else:
            reply_text = "Pardon?"
            reply_content.append(TextSendMessage(text=reply_text))

    elif status == GameState.ASKING:
        if message in ["はい", "いいえ"]:
            answer = Answer()
            answer.question = user_status.progress.latest_question
            answer.value = 1.0 if message == "はい" else -1.0
            user_status.progress.answers.append(answer)
            if len(user_status.progress.answers) < len(Question.query.all()):
                question = Question.query.all()[len(user_status.progress.answers)]
                user_status.progress.latest_question = question
                items = [
                    QuickReplyButton(action=MessageAction(label="はい", text="はい")),
                    QuickReplyButton(action=MessageAction(label="いいえ", text="いいえ")),
                ]
                reply_content.append(TextSendMessage(text=question.message, quick_reply=QuickReply(items=items)))
            else:
                user_status.status = GameState.PENDING.value
                reply_content.append(TextSendMessage(text="Fin"))
            db.session.add(user_status)
            db.session.commit()


    line.reply_message(event.reply_token, reply_content)

from fastapi import APIRouter, Request, BackgroundTasks

router = APIRouter()

@router.post("/webhook")
async def twilio_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint to receive incoming SMS from Twilio.
    """
    # form_data = await request.form()
    # background_tasks.add_task(process_sms, form_data)
    
    # Skeleton implementation always returns a 200 OK so Twilio doesn't retry
    return {"status": "received"}

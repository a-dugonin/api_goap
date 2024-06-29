from fastapi import FastAPI, HTTPException
from playhouse.shortcuts import model_to_dict
from models import (
    TicketCreate,
    Tickets,
    TicketUpdate,
    AlarmCreate,
    Alarms,
    create_models,
)

create_models()
app = FastAPI()


@app.post("/ticket")
async def create_ticket(ticket: TicketCreate) -> str:
    """Метод для создания записи в таблице tickets"""
    Tickets.create(ne_name=ticket.ne_name, status=ticket.status)
    return "Тикет успешно создан"


@app.patch("/ticket")
async def update_ticket(ticket: TicketUpdate) -> str:
    """Метод для обновления статуса тикета"""
    query = Tickets.update(status=ticket.status).where(
        Tickets.request_id == ticket.request_id
    )
    if query.execute():
        return "Статус тикета успешно обновлен"
    else:
        raise HTTPException(
            status_code=404, detail="Тикет с указанным id не существует"
        )


@app.post("/alarm")
async def create_alarm(alarm: AlarmCreate) -> str:
    """Метод для создания записи в таблице alarms"""
    Alarms.create(ne_name=alarm.ne_name)
    return "Аларм успешно создан"


@app.get("/ticket")
async def get_ticket(request_id: int) -> dict:
    """Метод для получения инцидента по request_id"""
    ticket = Tickets.select().where(Tickets.request_id == request_id).first()
    if not ticket:
        raise HTTPException(
            status_code=404, detail="Тикет с указанным id не существует"
        )

    ticket_dict = model_to_dict(ticket)
    ticket_dict["bts_alarms"] = []
    alarms_query = Alarms.select().where(Alarms.ne_name == ticket.ne_name)
    for alarm in alarms_query:
        ticket_dict["bts_alarms"].append(
            {
                key: value
                for key, value in model_to_dict(alarm).items()
                if key != "ne_name"
            }
        )

    return ticket_dict


@app.get("/tickets")
async def get_tickets() -> list:
    """Метод для получения всех тикетов"""
    tickets = Tickets.select()
    ticket_list = [model_to_dict(ticket) for ticket in tickets]
    return ticket_list

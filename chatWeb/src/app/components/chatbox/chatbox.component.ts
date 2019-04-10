import { Component, OnInit, Input, Output, EventEmitter, OnDestroy } from '@angular/core';
import { Contact } from '../../app.component';
import { ContactService } from '../../service/contacts.service';

export interface PostChat {
  data: PostChatContent;
}

export interface PostChatContent {
  sender: number;
  receiver: number;
  content: string;
}

export interface PostChatReturn {
  status: number;
  reason: string;
  currectid: number;
}

export interface GetRecordsReturn {
  status: number;
  reason: string;
  data: RecordFormt[];
}

export interface RecordFormt {
  id: number;
  sender: number;
  receiver: number;
  content: string;
  sendtime: string;
}

@Component({
  selector: 'app-chatbox',
  templateUrl: './chatbox.component.html',
  styleUrls: ['./chatbox.component.scss']
})

export class ChatboxComponent implements OnInit, OnDestroy {

  @Input()
  whoLogin: Contact;

  @Input()
  whoTouch: Contact;

  records: {
    sender: string,
    receiver: string,
    content: string,
    sendtime: string,
    id: number
  }[] = [];
  haveNewRecord: boolean;

  newRecords: {
    sender: string,
    receiver: string,
    content: string,
    sendtime: string
  }[] = [];

  public constructor(public contactService: ContactService) {}

  postChatReturn: PostChatReturn;
  currectId: number;
  inputContent: string;
  postData: PostChatContent;
  postContent: PostChat = {data: {sender: 0, receiver: 0, content: ''}};

  timerId: any;

  ngOnInit() {
    this.contactService.getLatestTenRecord(this.whoTouch.id, this.whoLogin.id).then(result => {
      this.records = result.data.map(value => ({
        sender : this.getContactName(value.sender),
        receiver : this.getContactName(value.receiver),
        content : value.content,
        sendtime : value.sendtime,
        id : value.id
      }));
      this.timerId = setInterval(() => {
        if (this.records.length !== 0) {
          const recordPromise = this.contactService.getNewRecord(
            this.whoLogin.id, this.whoTouch.id, this.records[this.records.length - 1].id);
          recordPromise.then(resultTwo => {
            const record = resultTwo.data.map(value => ({
              sender : this.getContactName(value.sender),
              receiver : this.getContactName(value.receiver),
              content : value.content,
              sendtime : value.sendtime,
              id : value.id
            }));
            this.records = this.records.concat(record);
          });
        }
      }, 1000);

    }, error => {
      console.log(error);
    });
  }

  ngOnDestroy() {
    if (this.timerId !== undefined) {
      clearInterval(this.timerId);
    }
  }

  public getContactName(id: number) {
      return [this.whoLogin, this.whoTouch].find(value => value.id === id).name;
  }

  sendClick() {
    this.postContent.data.sender = this.whoLogin.id;
    this.postContent.data.receiver = this.whoTouch.id;
    this.postContent.data.content = this.inputContent;
    this.contactService.postChatContent(this.postContent).then(result => {
      this.currectId = result.currectid;
    }, error => {
      console.log(error);
    });
  }

}

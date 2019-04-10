import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';
import { Contacts } from '../app.component';
import {PostChat, GetRecordsReturn, PostChatReturn} from '../components/chatbox/chatbox.component';


@Injectable({
  providedIn: 'root'
})
export class ContactService {

  public constructor(public http: HttpClient) { }

  public getContacts(): Promise<Contacts> {
    return this.http.get<Contacts>('http://127.0.0.1:7777/user/userlist').toPromise();
  }

  public getUserName(whoLoginId: number, reverseFlag: string): Promise<Contacts> {

    return this.http.get<Contacts>(`http://127.0.0.1:7777/user/username?id=${whoLoginId}&reverse=${reverseFlag}`).toPromise();
  }

  public postChatContent(postContent: PostChat): Promise<PostChatReturn> {
    return this.http.post<PostChatReturn>('http://127.0.0.1:7777/user/record', postContent).toPromise();

  }

  public getLatestTenRecord(receiver: number, sender: number): Promise<GetRecordsReturn> {
    return this.http.get<GetRecordsReturn>(`http://127.0.0.1:7777/user/records?sender=${sender}&receiver=${receiver}`).toPromise();

  }

  public getNewRecord(receiver: number, sender: number, latestchatId: number): Promise<GetRecordsReturn> {
    return this.http.get<GetRecordsReturn>
    (`http://127.0.0.1:7777/user/newrecords?sender=${sender}&receiver=${receiver}&latestchatid=${latestchatId}`).toPromise();

  }


}

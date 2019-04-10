import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Contact} from '../../app.component';
import { ContactService } from '../../service/contacts.service';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent implements OnInit {

  @Input()
  whoLogin: Contact;
  public otherContacts: Contact[];
  public whoContact: Contact;
  public latestTenRecords: JSON;
  constructor(public contactService: ContactService) {  }

  ngOnInit() {

    // 获取非登录用户名
    this.contactService.getUserName(this.whoLogin.id, 'true').then(result => {
      this.otherContacts = result.data;
    }, error => {
      console.log(error);
    });
  }
    // 点击用户后打开聊天框
  public contactClick(contact: Contact): void {
    this.whoContact = contact;
  }
}

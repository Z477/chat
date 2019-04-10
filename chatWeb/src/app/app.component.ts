import { Component , OnInit, Input, Output, EventEmitter} from '@angular/core';
import { ContactService } from './service/contacts.service';

export interface Contacts {
  status: number;
  reason: string;
  data: Contact[];
}
export interface Contact {
  id: number;
  name: string;
}

export interface PostLogin {
  status: number;
  reason: string;
  token: string;

}

export enum PageType {
  LoginPage = 'LoginPage',
  HomePage = 'HomePage',
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  // 组件里不能定义枚举，但可以通过赋值的方式获取枚举型
  public pageTypeEnum = PageType;
  public contacts: Contact[] = [];
  public whoLoginId: number;
  public whoLogin: Contact;
  public curPageType: PageType = PageType.LoginPage;

  // 注入service，只能在构造函数里注入服务
  public constructor(public contactService: ContactService) {}

  // 当该组件被angular初始化好以后，就会调用钩子函数ngOnInit()
  // 一般都在钩子函数里去执行自定义的初始化过程， 而不在构造函数里，以防组件没有被初始化完整
  public ngOnInit(): void {
    this.contactService.getContacts().then(result => {
      this.contacts = result.data;
    }, error => {
      console.log(error);
    });
  }

  public loginClick(): void {
      this.curPageType = PageType.HomePage;
  }

  public setWhoLoginId(id: string): void {
    this.whoLoginId = Number.parseInt(id, 10);
    this.whoLogin = this.contacts.find(value => value.id === this.whoLoginId);
  }
}

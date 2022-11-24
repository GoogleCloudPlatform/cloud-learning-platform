import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-show-more',
  templateUrl: './show-more.component.html',
  styleUrls: ['./show-more.component.scss']
})
export class ShowMoreComponent implements OnInit {
  @Input() descText: string
  @Input() letters: number
  mode: string = 'more'
  tempString: string
  constructor() { }

  ngOnInit(): void {
    this.tempString = this.descText
    this.descText = this.descText.slice(0, this.letters)
  }
  show(mode: string) {
    if (mode == 'more') {
      this.descText = this.tempString
      this.mode = 'less'
    }
    else if (mode == 'less') {
      this.descText = this.descText.slice(0, this.letters)
      this.mode = 'more'
    }
  }
}

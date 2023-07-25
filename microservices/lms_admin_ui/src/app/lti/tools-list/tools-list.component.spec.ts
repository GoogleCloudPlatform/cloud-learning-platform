import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { DeleteLtiDialog, ToolsListComponent, ViewLtiDialog } from './tools-list.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { LtiService } from '../service/lti.service';
import { of } from 'rxjs';
import { By } from '@angular/platform-browser';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { MatLegacyTableDataSource as MatTableDataSource } from '@angular/material/legacy-table'
import { MatTableModule } from '@angular/material/table';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('ToolsListComponent', () => {
  let component: ToolsListComponent;
  let fixture: ComponentFixture<ToolsListComponent>;
  let ltiService : LtiService
  let dialog : MatDialog;
  let mockToolResponse = {
    "success": true,
    "message": "Tools has been fetched successfully",
    "data": [
        {
            "name": "Harmonize Google Dev",
            "description": "Test integration with Harmonize google dev tool",
            "tool_url": "https://google-lti-dev.customer.42lines.net",
            "tool_login_url": "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc11ac334bd48e463a227f0d57/initiation",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://google-lti-dev-001.customer.42lines.net/.well-known/e00bc11ac334bd48e463a227f0d57/jwks.json",
            "content_selection_url": "https://google-lti-dev-001.customer.42lines.net/lti/v13/e00bc11ac334bd48e463a227f0d57/harmonize/resource/omni/builder",
            "redirect_uris": [
                "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc11ac334bd48e463a227f0d57/target"
            ],
            "enable_grade_sync": false,
            "enable_nrps": true,
            "custom_params": "deepLinkLaunchEndpoint=$ResourceLink.RelaunchURL;timezone=$Person.address.timezone;prevContexts=$Context.id.history",
            "validate_title_for_grade_sync": false,
            "deeplink_type": "Allow everytime",
            "id": "xwsBdJzESQWiQw7Plh",
            "client_id": "db5e95d-87a3-49d8-9b3f-ad95c934705",
            "deployment_id": "d14100f-e817-4e55-b1a4-63fe916cb3e",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-06-07 13:28:45.285146+00:00",
            "last_modified_time": "2023-06-07 13:56:47.149432+00:00"
        },
        {
            "name": "Insribe preprod",
            "description": "Insribe preprod test tool integration",
            "tool_url": "https://preprod.icribe.education",
            "tool_login_url": "https://preprod.inscribe.education/organizations/asu/lti13/login",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://preprod.inscribe.education/oauth2/jwks",
            "content_selection_url": null,
            "redirect_uris": [
                "https://preprod.inscribe.education/organizations/asu/lti13/launch"
            ],
            "enable_grade_sync": false,
            "enable_nrps": false,
            "custom_params": "",
            "validate_title_for_grade_sync": false,
            "deeplink_type": "Allow everytime",
            "id": "Owxks4epc9CydOwtb8",
            "client_id": "8861ff1-f0c0-4870-b8c8-828f5fb0e2c",
            "deployment_id": "4f55186-9af0-4471-a125-e45d8b68514",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-04-06 16:46:44.783228+00:00",
            "last_modified_time": "2023-04-06 16:46:44.783228+00:00"
        }
    ]
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, NgxSkeletonLoaderModule, MatTableModule, BrowserAnimationsModule],
      declarations: [ ToolsListComponent , ViewLtiDialog, DeleteLtiDialog],
      providers: [ MatDialog, LtiService,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close']) },
        { provide: MAT_DIALOG_DATA, useValue:  {id: 1, name: 'ABC'}} // for DeleteLtiDialog
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ToolsListComponent);
    component = fixture.componentInstance;
    ltiService = TestBed.inject(LtiService);
    component.dataSource = new MatTableDataSource(component.ltiToolsData);
    dialog = TestBed.inject(MatDialog)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call fetchLtiTools method, update ltiToolsData and render tools in UI', fakeAsync(()=>{
    spyOn(ltiService, 'getToolsList').and.returnValue(of(mockToolResponse))
    component.fetchLtiTools()
    fixture.detectChanges()
    expect(ltiService.getToolsList).toHaveBeenCalled()
    expect(JSON.stringify(component.ltiToolsData)).toEqual(JSON.stringify(mockToolResponse.data))
    tick(1000)
    expect(component.isLoadingData).toBeFalsy()
    fixture.detectChanges()
    const tableDebugElement = fixture.debugElement.query(By.css('table tbody'));
    const tableElement: HTMLTableElement = tableDebugElement.nativeElement;
    expect(tableElement.rows[0].cells[0].textContent.trim()).toBe(component.ltiToolsData[0]['client_id'])
    expect(tableElement.rows[0].cells[1].textContent.trim()).toBe(component.ltiToolsData[0]['name'])
    expect(tableElement.rows[0].cells[2].textContent.trim()).toBe(component.ltiToolsData[0]['description'])
  }))

  it('should call openViewToolDialog and open dialog when clicked on eye icon', fakeAsync(()=>{
    spyOn(ltiService, 'getToolsList').and.returnValue(of(mockToolResponse))
    component.fetchLtiTools()
    tick(1000)
    fixture.detectChanges()
    const tableDebugElement = fixture.debugElement.query(By.css('table tbody'));
    const tableElement: HTMLTableElement = tableDebugElement.nativeElement;
    const buttonElement  = tableElement.rows[0].cells[3].getElementsByTagName('span') // get buttons

    spyOn(component, 'openViewToolDialog') // spy on openViewToolDialog function
    buttonElement.item(0).click() // click on eye button
    expect(component.openViewToolDialog).toHaveBeenCalled()
  }))

  it('should call openUpdateToolDialog open edit dialog when clicked on pencil icon', fakeAsync(()=>{
    spyOn(ltiService, 'getToolsList').and.returnValue(of(mockToolResponse))
    component.fetchLtiTools()
    tick(1000)
    fixture.detectChanges()
    const tableDebugElement = fixture.debugElement.query(By.css('table tbody'));
    const tableElement: HTMLTableElement = tableDebugElement.nativeElement;
    const buttonElement  = tableElement.rows[0].cells[3].getElementsByTagName('span') // get buttons
    spyOn(component, 'openUpdateToolDialog') // spy on openUpdateToolDialog function
    buttonElement.item(1).click() // click on pencil button
    expect(component.openUpdateToolDialog).toHaveBeenCalled()
  }))

  it('should call openDeleteDialog when clicked on delete icon', fakeAsync(()=>{
    spyOn(ltiService, 'getToolsList').and.returnValue(of(mockToolResponse))
    component.fetchLtiTools()
    tick(1000)
    fixture.detectChanges()
    const tableDebugElement = fixture.debugElement.query(By.css('table tbody'));
    const tableElement: HTMLTableElement = tableDebugElement.nativeElement;
    const buttonElement  = tableElement.rows[0].cells[3].getElementsByTagName('span') // get buttons
    spyOn(component, 'openDeleteDialog') // spy on openDeleteDialog function
    buttonElement.item(2).click() // click on delete button
    expect(component.openDeleteDialog).toHaveBeenCalled()
  }))

  it('in DeleteLtiDialog should call deleteTool ', ()=>{
    const mockResponse = {success: true}
    let fixture = TestBed.createComponent(DeleteLtiDialog);
    let component = fixture.componentInstance;
    component.deleteDialogData = TestBed.inject(MAT_DIALOG_DATA)
    fixture.detectChanges()

    const toolName = fixture.debugElement.query(By.css('b'))
    expect(toolName.nativeElement.textContent).toBe(component.deleteDialogData.name) // Should be 'ABC'

    const confimButtons = fixture.debugElement.queryAll(By.css('.mat-dialog-actions button'))
    const yesButton = confimButtons[1] // Yes button to call deleteTool method
    spyOn(ltiService, 'deleteTool').and.returnValue(of(mockResponse))
    yesButton.nativeElement.click()
    expect(ltiService.deleteTool).toHaveBeenCalled()
  })

});

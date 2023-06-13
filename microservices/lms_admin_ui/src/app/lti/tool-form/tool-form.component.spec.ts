import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ToolFormComponent } from './tool-form.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field'; // Import MatFormFieldModule separately
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatOption, MatOptionModule } from '@angular/material/core';
import { MatSelect, MatSelectModule } from '@angular/material/select';

import { LtiService } from '../service/lti.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { By } from '@angular/platform-browser';

fdescribe('ToolFormComponent', () => {
  let component: ToolFormComponent;
  let fixture: ComponentFixture<ToolFormComponent>;
  let ltiService: LtiService;
  let fb : FormBuilder;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, ReactiveFormsModule,MatOptionModule,
        MatFormFieldModule, MatCheckboxModule, MatInputModule, MatIconModule, MatMenuModule, MatSelectModule,BrowserAnimationsModule],
      declarations: [ ToolFormComponent ],
      providers: [FormBuilder,FormControl, Validators,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: '', extra_data:{} }}
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ToolFormComponent);
    component = fixture.componentInstance;
    component.dialogData = TestBed.inject(MAT_DIALOG_DATA)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should identify elements and input values in the form' ,()=>{
    const mockData = {
      "name": "Harmonize Google Dev",
      "description": "Test integration with Harmonize google dev tool",
      "tool_url": "https://google-lti-dev-01.customer.42lines.net",
      "tool_login_url": "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc131ac33bd48e44b6a227f0d57/initiation",
      "public_key_type": "JWK URL",
      "tool_public_key": null,
      "tool_keyset_url": "https://google-lti-dev-001.customer.42lines.net/.well-known/e00bc131ac33bd48e44b6a227f0d57/jwks.json",
      "content_selection_url": "https://google-lti-dev-001.customer.42lines.net/lti/v13/e00bc131ac33bd48e44b6a227f0d57/harmonize/resource/omni/builder",
      "redirect_uris": [
          "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc131ac33bd48e44b6a227f0d57/target"
      ],
      "enable_grade_sync": false,
      "enable_nrps": true,
      "custom_params": "deepLinkLaunchEndpoint=$ResourceLink.RelaunchURL;timezone=$Person.address.timezone;prevContexts=$Context.id.history",
      "validate_title_for_grade_sync": false,
      "deeplink_type": "Allow everytime",
      "id": "xwsBdJzPESMQWiQw7Plh",
      "client_id": "db5e95d-87a3-49d8-9b3f-ad95c194705",
      "deployment_id": "d14300f-e817-4e55-b1a4-63fe906cb3e",
      "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
      "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
      "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
      "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
      "created_time": "2023-06-07 13:28:45.285146+00:00",
      "last_modified_time": "2023-06-07 13:56:47.149432+00:00"
    }
    // create tool heading
    const headingElement = fixture.debugElement.query(By.css('h1'))
    expect(headingElement.nativeElement.textContent.toLowerCase().trim()).toBe('Create Tool')
    // insert in name input field
    const nameElement = fixture.debugElement.query(By.css(`input[formControlName='name']`));
    const nameInput = nameElement.nativeElement as HTMLInputElement;
    nameInput.value =  mockData.name;
    nameInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    // insert in description input field
    const descriptionElement = fixture.debugElement.query(By.css(`input[formControlName='description']`));
    const descriptionInput = descriptionElement.nativeElement as HTMLInputElement;
    descriptionInput.value =  mockData.description;
    descriptionInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    // insert in tool_url input field
    const tool_urlElement = fixture.debugElement.query(By.css(`input[formControlName='tool_url']`));
    const tool_urlInput = tool_urlElement.nativeElement as HTMLInputElement;
    tool_urlInput.value =  mockData.tool_url;
    tool_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    // insert in tool_login_url input field
    const tool_login_urlElement = fixture.debugElement.query(By.css(`input[formControlName='tool_login_url']`));
    const tool_login_urlInput = tool_login_urlElement.nativeElement as HTMLInputElement;
    tool_login_urlInput.value =  mockData.tool_login_url;
    tool_login_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    // By default 'JWK URL' option selected
    const public_key_typeElement = fixture.debugElement.query(By.css(`mat-select[formControlName='public_key_type']`));
    const public_key_typeInput = public_key_typeElement.componentInstance as MatSelect;
    const expectedValue =  mockData.public_key_type;
    // const options = public_key_typeElement.queryAll(By.directive(MatOption));
    // // Find and select the desired option
    // const desiredOption = options.find((option) => option.nativeElement.textContent.trim() === expectedValue);
    // public_key_typeInput.value = desiredOption.componentInstance.value;
    // public_key_typeInput.writeValue(public_key_typeInput.value);
    // fixture.detectChanges();

    // Retrieve the selected value
    const selectedValue = public_key_typeInput.value;
    expect(selectedValue).toEqual(expectedValue);
    //Insert in tool_keyset_url input field
    const tool_keyset_url = fixture.debugElement.query(By.css(`input[formControlName='tool_keyset_url']`));
    const tool_keyset_urlInput = tool_keyset_url.nativeElement as HTMLInputElement;
    tool_keyset_urlInput.value =  mockData.tool_keyset_url;
    tool_keyset_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    //Insert in content_selection_url input field
    const content_selection_urlElement = fixture.debugElement.query(By.css(`input[formControlName='content_selection_url']`));
    const content_selection_urlInput = content_selection_urlElement.nativeElement as HTMLInputElement;
    content_selection_urlInput.value =  mockData.content_selection_url;
    content_selection_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    //Insert in redirect_uris textarea 
    // const redirect_urisElement = fixture.debugElement.query(By.css(`textarea[formControlName='redirect_uris']`));
    // const redirect_urisInput = redirect_urisElement.nativeElement as HTMLTextAreaElement;
    // redirect_urisInput.value =  mockData.redirect_uris;
    // redirect_urisInput.dispatchEvent(new Event('input'));
    // fixture.detectChanges();
  })
});

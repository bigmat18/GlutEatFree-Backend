from re import M
import pytest


def test_paragraph_create(client, access_authorization, article):
        
    response = client.post(f"/article/{article.slug}/paragraphs", 
                            files={"images": ("filename", open("information.txt", "rb"), "image/jpeg")},
                            data={"title": "test", "content": "test", "captions": ["test"]},
                            headers=access_authorization)
    assert response.status_code == 201
    assert len(response.json()["images"]) == 1
    assert response.json()["images"][0]["caption"] != None
    
def test_paragraph_create_unauth(client, unauth_authorization, article):
    response = client.post(f"/article/{article.slug}/paragraphs", 
                           data={"title": "test", "content": "title"},
                           headers=unauth_authorization)
    assert response.status_code == 401



def test_paragraph_list(client, access_authorization, article):
    response = client.get(f"/article/{article.slug}/paragraphs",
                           headers=access_authorization)
    assert response.status_code == 200



def test_paragraph_retrieve(client, access_authorization, paragraph):
    response = client.get(f"/article/paragraph/{paragraph.id}", 
                           headers=access_authorization)
    assert response.status_code == 200



def test_paragraph_update(client, access_authorization, paragraph):
    response = client.patch(f"/article/paragraph/{paragraph.id}", 
                           data={"title": "new title"},
                           headers=access_authorization)
    assert response.status_code == 200

def test_paragraph_update_unauth(client, unauth_authorization, paragraph):
    response = client.patch(f"/article/paragraph/{paragraph.id}", 
                           data = {"title": "new title"},
                           headers=unauth_authorization)
    assert response.status_code == 401



def test_paragraph_delete(client, access_authorization, paragraph):
    response = client.delete(f"/article/paragraph/{paragraph.id}",
                           headers=access_authorization)
    assert response.status_code == 204

def test_paragraph_delete_unauth(client, unauth_authorization, paragraph):
    response = client.delete(f"/article/paragraph/{paragraph.id}", 
                           headers=unauth_authorization)
    assert response.status_code == 401



def test_paragraph_image_update(client, access_authorization, paragraph_image):
    response = client.patch(f"/article/paragraph/image/{paragraph_image.id}",
                             data={"caption": "new test"},
                             headers=access_authorization)
    assert response.status_code == 200

def test_paragraph_image_update_unauth(client, unauth_authorization, paragraph_image):
    response = client.patch(f"/article/paragraph/image/{paragraph_image.id}",
                             data={"caption": "new test"},
                             headers=unauth_authorization)
    assert response.status_code == 401



def test_paragraph_image_create(client, access_authorization, paragraph):
    with open('information.txt', "rb") as file:
        response = client.post(f"/article/paragraph/{paragraph.id}/image",
                               files={"images": file, "caption": "test"},
                               headers=access_authorization)
        assert response.status_code == 201
        assert response.json()[0]['image'] != "" 

def test_paragraph_image_create_unauth(client, unauth_authorization, paragraph):
    with open('information.txt', "rb") as file:
        response = client.post(f"/article/paragraph/{paragraph.id}/image",
                               files={"images": file, "caption": "test"},
                               headers=unauth_authorization)
        assert response.status_code == 401




def test_paragraph_image_delete(client, access_authorization, paragraph_image):
    response = client.delete(f"/article/paragraph/image/{paragraph_image.id}",
                             headers=access_authorization)
    assert response.status_code == 204

def test_paragraph_image_delete_unauth(client, unauth_authorization, paragraph_image):
    response = client.delete(f"/article/paragraph/image/{paragraph_image.id}",
                             headers=unauth_authorization)
    assert response.status_code == 401
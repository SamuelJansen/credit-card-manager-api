import os, json

from python_helper import Constant as c
from python_helper import ObjectHelper, EnvironmentHelper, StringHelper, FileOperation, FileHelper, log
from python_framework import Repository, Serializer

from domain import AuthorizationAccess


class FileManager:

    def __init__(self):
        self.filename = 'security.json'
        self.fileUri = 'security'
        self.uri = os.path.join(f'api{EnvironmentHelper.OS_SEPARATOR}src{EnvironmentHelper.OS_SEPARATOR}repository', self.fileUri)
        if not os.path.isdir(self.uri):
            os.mkdir(self.uri)
        self.filepath = os.path.join(self.uri, self.filename)

    def writeContent(self, content):
        try:
            FileHelper.writeContent(self.filepath, content, operation=FileOperation.OVERRIDE_TEXT)
            return content
        except Exception as exception:
            log.failure(self.writeContent, f'Not possible to write content. Filepath: {self.filepath}, content: {content}, operation: {FileOperation.OVERRIDE_TEXT}', exception=exception)
            raise exception


    def readContent(self):
        try:
            return StringHelper.join(
                StringHelper.join(
                    FileHelper.getFileLines(self.filepath),
                    character = c.BLANK
                ).replace(c.NEW_LINE, c.BLANK).split(),
                character = c.BLANK
            )
        except Exception as exception:
            log.failure(self.readContent, f'Not possible to read content. Filepath: {self.filepath}', exception=exception)
            raise exception


@Repository(model = AuthorizationAccess.AuthorizationAccess)
class SecurityRepository:

    manager = FileManager()

    def writeAccesses(self, accesses):
        self.manager.writeContent(StringHelper.prettyJson(Serializer.getObjectAsDictionary(accesses)))


    def readAccesses(self):
        content = self.manager.readContent()
        if ObjectHelper.isNoneOrBlank(content):
            return []
        return Serializer.convertFromJsonToObject(
            Serializer.convertFromJsonToDictionary(content),
            [[self.model]]
        )
